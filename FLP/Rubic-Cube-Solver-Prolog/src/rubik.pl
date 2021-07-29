/** 
    FLP 2021 - Rubik's Cube 
    autor: Ondrej Sajdik (xsajdi01)
*/

%  Rotate right around face center
rotate1([ 
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
    [[X64,X65,X66]],
    [[X67,X68,X69]]
],[
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X49,X46,X43]],
    [[X17,X14,X11],[X57,X22,X23],[X31,X32,X33],[X41,X42,X61]],
    [[X18,X15,X12],[X58,X25,X26],[X34,X35,X36],[X44,X45,X62]],
    [[X19,X16,X13],[X59,X28,X29],[X37,X38,X39],[X47,X48,X63]], 
    [[X27,X24,X21]],
    [[X64,X65,X66]],
    [[X67,X68,X69]]
]).
rotate2(
[
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
    [[X64,X65,X66]],
    [[X67,X68,X69]]
],[
    [[X51,X52,X13]],
    [[X54,X55,X16]],
    [[X57,X58,X19]],
    [[X11,X12,X63],[X27,X24,X21],[X59,X32,X33],[X41,X42,X43]],
    [[X14,X15,X66],[X28,X25,X22],[X56,X35,X36],[X44,X45,X46]],
    [[X17,X18,X69],[X29,X26,X23],[X53,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X37]],
    [[X64,X65,X34]],
    [[X67,X68,X31]]
]).
rotate3([
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
	[[X64,X65,X66]],
    [[X67,X68,X69]]
],[
    [[X23,X26,X29]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X69],[X37,X34,X31],[X53,X42,X43]],
    [[X14,X15,X16],[X24,X25,X68],[X38,X35,X32],[X52,X45,X46]],
    [[X17,X18,X19],[X27,X28,X67],[X39,X36,X33],[X51,X48,X49]], 
    [[X61,X62,X63]],
    [[X64,X65,X66]],
    [[X41,X44,X47]]
]).
rotate4([
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
	[[X64,X65,X66]],
    [[X67,X68,X69]]
],[
    [[X39,X52,X53]],
    [[X36,X55,X56]],
    [[X33,X58,X59]],
    [[X51,X12,X13],[X21,X22,X23],[X31,X32,X67],[X47,X44,X41]],
    [[X54,X15,X16],[X24,X25,X26],[X34,X35,X64],[X48,X45,X42]],
    [[X57,X18,X19],[X27,X28,X29],[X37,X38,X61],[X49,X46,X43]], 
    [[X11,X62,X63]],
	[[X14,X65,X66]],
    [[X17,X68,X69]]
]).
rotate5([
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
	[[X64,X65,X66]],
    [[X67,X68,X69]]
],
[
    [[X57,X54,X51]],
    [[X58,X55,X52]],
    [[X59,X56,X53]],
    [[X21,X22,X23],[X31,X32,X33],[X41,X42,X43],[X11,X12,X13]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
	[[X64,X65,X66]],
    [[X67,X68,X69]]
]).
rotate6([
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X17,X18,X19],[X27,X28,X29],[X37,X38,X39],[X47,X48,X49]], 
    [[X61,X62,X63]],
	[[X64,X65,X66]],
    [[X67,X68,X69]]
],[
    [[X51,X52,X53]],
    [[X54,X55,X56]],
    [[X57,X58,X59]],
    [[X11,X12,X13],[X21,X22,X23],[X31,X32,X33],[X41,X42,X43]],
    [[X14,X15,X16],[X24,X25,X26],[X34,X35,X36],[X44,X45,X46]],
    [[X47,X48,X49],[X17,X18,X19],[X27,X28,X29],[X37,X38,X39]], 
    [[X67,X64,X61]],
	[[X68,X65,X62]],
    [[X69,X66,X63]]
]).


/* Predicates from example */
/****************************************************************/
read_line(L,C) :-
	get_char(C),
	(isEOFEOL(C), L = [], !;
		read_line(LL,_),% atom_codes(C,[Cd]),
		[C|LL] = L).


isEOFEOL(C) :-
	C == end_of_file;
	(char_code(C,Code), Code==10).


read_lines(Ls) :-
	read_line(L,C),
	( C == end_of_file, Ls = [] ;
	  read_lines(LLs), Ls = [L|LLs]
	).


split_line([],[[]]) :- !.
split_line([' '|T], [[]|S1]) :- !, split_line(T,S1).
split_line([32|T], [[]|S1]) :- !, split_line(T,S1).    
split_line([H|T], [[H|G]|S1]) :- split_line(T,[G|S1]). 

split_lines([],[]).
split_lines([L|Ls],[H|T]) :- split_lines(Ls,T), split_line(L,H).
/**********************************************************************/

/** Print Cubes */
write_cubes([H|[]]) :- write_cube(H). 
write_cubes([H|T]) :- write_cube(H), nl, write_cubes(T).

/** Print Cube */
write_cube([H|[]]) :- write_cube_line(H), nl. 
write_cube([H|T]) :- write_cube_line(H), nl, write_cube(T).
write_cube_line([H|[]]) :- write_cube_row(H).
write_cube_line([H|T]) :- write_cube_row(H), write(' '), write_cube_line(T).
write_cube_row([H|[]]) :- write(H).
write_cube_row([H|T]) :- write(H), write_cube_row(T).

/** Check if cube is solved then return solved */
step([ 
    [[A,A,A]],
    [[A,A,A]],
    [[A,A,A]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]], 
    [[F,F,F]],
    [[F,F,F]],
    [[F,F,F]]
], _ , _ , [[ 
    [[A,A,A]],
    [[A,A,A]],
    [[A,A,A]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]],
    [[B,B,B],[C,C,C],[D,D,D],[E,E,E]], 
    [[F,F,F]],
    [[F,F,F]],
    [[F,F,F]]
]]).
/** if not solve rotate cube and return path to solved cube */
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate1(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate2(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate3(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate4(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate5(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate6(Cube, Cube_new), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate1(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate2(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate3(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate4(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate5(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).
step(Cube, Depth, MaxDepth, [Cube|Res]) :- Depth<MaxDepth, rotate6(Cube_new, Cube), step(Cube_new, Depth+1, MaxDepth, Res).

/** IDS */
find_solution(Cube,MaxDepth, Res):- step(Cube, 0, MaxDepth, Res).
find_solution(Cube,MaxDepth, Res):- find_solution(Cube, MaxDepth+1, Res).

/** Main */
start :-
        prompt(_, ''),
		read_lines(LL),
		split_lines(LL,Cube),
		find_solution(Cube, 1, Solution),
		write_cubes(Solution),
		halt.
