/*
 * algorithm: pipeline sort
 * author: Ondrej Sajdik
 *
 */

#include <mpi.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <queue>

using namespace std;

#define FILENAME "numbers"

int main(int argc, char *argv[])
{
    int numprocs;               
    int myid;                   
    MPI_Status stat;  
    MPI_Init(&argc,&argv);                          
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);       
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);           
    int n = pow(2, (numprocs-1));

    if(myid == 0){  // first processor 
        int number;
        fstream f;
        f.open(FILENAME, ios::in);

        if(f.good()) number = f.get();
        if(f.good()){
            cout << number;
            MPI_Send(&number, 1, MPI_INT, myid+1, 0, MPI_COMM_WORLD);
        } 

        while(f.good()){
            number = f.get();
            if(!f.good()) break; 
            cout << " " << number;
            MPI_Send(&number, 1, MPI_INT, myid+1, 0, MPI_COMM_WORLD);
        }

        cout << endl;
        f.close();

    }
    else if(myid == numprocs-1){ // last processor
        int num;
        queue<int> q0;
        queue<int> q1;
        int sizeOfInput = pow(2, myid-1);

        int from0 = sizeOfInput;
        int from1 = sizeOfInput;

        for (int i = 0; i< sizeOfInput;i++){
            MPI_Recv(&num, 1, MPI_INT, myid-1, 0, MPI_COMM_WORLD, &stat);
            q0.push(num);
        }

        int loadingQueue = 1;
        int toLoadTotal = n - sizeOfInput;
        int toLoad = sizeOfInput;
        for(int i = 0 ; i < n;i++){
            // load 1 input
            if(toLoadTotal > 0){
                MPI_Recv(&num, 1, MPI_INT, myid-1, 0, MPI_COMM_WORLD, &stat);
                toLoadTotal--;

                if(loadingQueue){
                    q1.push(num);

                }else{
                    q0.push(num);
                }
                if(!(--toLoad)){
                    toLoad = sizeOfInput;
                    loadingQueue = !loadingQueue;
                }

            }
            // send 1 output 
            if(from0 && from1){
                if (q1.front() > q0.front()){
                    num = q0.front();
                    q0.pop();
                    from0--;
                }else{
                    num = q1.front();
                    q1.pop();
                    from1--;
                }

            }else if (from0){
                num = q0.front();
                q0.pop();
                from0--;
            }else if (from1){
                num = q1.front();
                q1.pop();
                from1--;
            }

            cout << num << endl;
            if(!from0 && !from1){
                from0 = from1 = sizeOfInput;
            }
        }
        
    }
    else{ // middle processors
        int num;
        int sizeOfInput = pow(2, myid-1);
        int from0 = sizeOfInput;
        int from1 = sizeOfInput;

        queue<int> q0;
        queue<int> q1;

        // init
        // load first sequence
        for (int i = 0; i< sizeOfInput;i++){
            MPI_Recv(&num, 1, MPI_INT, myid-1, 0, MPI_COMM_WORLD, &stat);
            q0.push(num);
        }

        int loadingQueue = 1;
        int toLoadTotal = n - sizeOfInput;
        int toLoad = sizeOfInput;
        for(int i = 0 ; i < n ; i++){
            // load 1 input
            if(toLoadTotal > 0){
                MPI_Recv(&num, 1, MPI_INT, myid-1, 0, MPI_COMM_WORLD, &stat);
                toLoadTotal--;
                if(loadingQueue){
                    q1.push(num);

                }else{
                    q0.push(num);
                }
                if(--toLoad == 0){
                    toLoad = sizeOfInput;
                    loadingQueue = !loadingQueue;
                }

            }
            // send 1 output 
            if(from0 && from1){
                if (q1.front() > q0.front()){
                    num = q0.front();
                    q0.pop();
                    from0--;
                }else{
                    num = q1.front();
                    q1.pop();
                    from1--;
                }

            }else if (from0){
                num = q0.front();
                q0.pop();
                from0--;

            }else if (from1){
                num = q1.front();
                q1.pop();
                from1--;
            }
            MPI_Send(&num, 1, MPI_INT, myid+1, 0, MPI_COMM_WORLD);
            if(!from0 && !from1){
                from0 = from1 = sizeOfInput;
            }
        }
    }
    
    MPI_Finalize(); 
    return 0;

}//main
