/*
 * Algorithm: Mesh Multiplication
 * Author: Ondrej Sajdik
 */

#include <mpi.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>

using namespace std;

#define MAT1_FILE "mat1"
#define MAT2_FILE "mat2"
#define ROW_INPUT_TAG 0
#define COL_INPUT_TAG 1
#define RESULT_TAG 2

int getRowSenderId(int myRow, int myCol, int colCount){
    if(myRow == 0){
        return myRow*colCount + myCol;
    }else{
        return (myRow-1)*colCount + myCol;
    }
}

int getColSenderId(int myRow, int myCol, int colCount){
    if(myCol == 0){
        return myRow*colCount + myCol;
    }else{
        return myRow*colCount + myCol- 1;
    }
}
int getRowReceiver(int myRow, int myCol, int colCount){
    return (myRow+1)*colCount + myCol;
}

int getColReceiver(int myRow, int myCol, int colCount){
    return myRow*colCount + myCol + 1;
}

vector<int> readCol(string filename, int colIndex){
    ifstream f;
    f.open(filename, ios::in);
    vector<int> values;
    string line;
    getline(f, line); // remove first line
    while(getline(f, line)){
        istringstream is(line);
        int num;
        for(int i = 0; i <= colIndex;i++){
            is >> num;
        }
        values.push_back(num);
    }
    return values;
}

vector<int> readRow(string filename, int rowIndex){
    ifstream f;
    f.open(filename, ios::in);
    vector<int> values;
    string line;
    getline(f, line); // remove first line
    for(int i = 0; i <= rowIndex;i++){
        getline(f, line);
    }
    istringstream is(line);
    int num;
    while(is >> num){
        values.push_back(num);
    }
    return values;
}

int main(int argc, char *argv[])
{
    int numprocs;               
    int myid;          
    int rows, cols, iterations;
    MPI_Status stat;  
    MPI_Init(&argc,&argv);                          
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);       
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);           
    
    //read output sizes
    if(myid == 0){
        string s;
        ifstream f1;
        ifstream f2;
        f1.open("mat1", ios::in);
        f2.open("mat2", ios::in);
        getline(f1, s);
        rows = stoi(s, nullptr, 10);
        getline(f2, s);
        cols = stoi(s, nullptr, 10);
        f1.close();
        f2.close();
    }

    // share output sizes
    MPI_Bcast(&cols, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&rows, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    // calculate my position
    int myCol = myid%cols;
    int myRow = myid/cols;
    
    // send input 
    if(myRow == 0){
        vector<int> col = readCol(MAT2_FILE, myCol);
        for(auto it = begin(col); it != end(col); it++){
            MPI_Send(&(*it), 1, MPI_INT, myid, ROW_INPUT_TAG, MPI_COMM_WORLD);
        }
        iterations = col.size();
    }
    if(myCol == 0){
        vector<int> row = readRow(MAT1_FILE, myRow);
        for(auto it = begin(row); it != end(row); it++){
            MPI_Send(&(*it), 1, MPI_INT, myid, COL_INPUT_TAG, MPI_COMM_WORLD);
        }
    }

    // share number of iterations
    MPI_Bcast(&iterations, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // start time measurement
    struct timespec begin, end; 
    if(myid == 0){
        clock_gettime(CLOCK_REALTIME, &begin);
    }


    // multiplicate
    int result = 0;
    for(int i = 0; i < iterations ;i++){
        // receive numbers
        int rowNum,colNum;
        MPI_Recv(&rowNum, 1, MPI_INT, getRowSenderId(myRow, myCol, cols), ROW_INPUT_TAG, MPI_COMM_WORLD, &stat);
        MPI_Recv(&colNum, 1, MPI_INT, getColSenderId(myRow, myCol, cols), COL_INPUT_TAG, MPI_COMM_WORLD, &stat);

        // calculate with numbers
        result+= rowNum*colNum ;

        // send numbers
        if(myRow + 1 != rows){
            MPI_Send(&rowNum, 1, MPI_INT, getRowReceiver(myRow, myCol, cols), ROW_INPUT_TAG, MPI_COMM_WORLD);
        }
        if(myCol + 1 != cols){
            MPI_Send(&colNum, 1, MPI_INT, getColReceiver(myRow, myCol, cols), COL_INPUT_TAG, MPI_COMM_WORLD);
        }
    }
    //send result
    MPI_Send(&result, 1, MPI_INT, 0, RESULT_TAG, MPI_COMM_WORLD);

    //print all results 
    if(myid == 0){
        cout << rows << ":" << cols << endl;
        for(int row = 0; row < rows; row++){
            MPI_Recv(&result, 1, MPI_INT, (row*cols),RESULT_TAG, MPI_COMM_WORLD,&stat);
            cout << result;
            for(int col = 1; col < cols;col++){
                int result;
                MPI_Recv(&result, 1, MPI_INT, (row*cols + col),RESULT_TAG, MPI_COMM_WORLD,&stat);
                cout << " " << result;
            }
            cout << endl;
        }
        // end time measurement and print 
        clock_gettime(CLOCK_REALTIME, &end);
        long seconds = end.tv_sec - begin.tv_sec;
        long nanoseconds = end.tv_nsec - begin.tv_nsec;
        double elapsed = seconds + nanoseconds*1e-9;
        // cout << elapsed << endl;
    }

    MPI_Finalize(); 
    return 0;

}//main
