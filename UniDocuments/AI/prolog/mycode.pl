%Yuta Sato z5186797 Artificial Intelligence Ass1 mycode.pl

%write a predicate sumsq_even(Numbers,Sum) that sums the squares of only
%the even numbers in a list of integers.

sum_list([], 0).
sum_list([H|T], Sum) :-
   sum_list(T, Rest),
   Sum is H * H + Rest.

remove_odd([],[]).
remove_odd([H|T],List):-
  H mod 2 =\= 0,
  remove_odd(T,List).
remove_odd([H|T1],[H|T2]):-
  H mod 2 =:= 0,
  remove_odd(T1,T2).

%sumsq_even([],0).
sumsq_even(List,Sum):-
  remove_odd(List,Even_List),
  sum_list(Even_List,Sum).

%We assume that each person will have the same family name as their father
%but that married woman retain their original birth name.
%Write a predicate same_name(Person1,Person2) that suceeds if it can be deducted
%from the facts in the database that person1 and person2 will have the same family name.
%It is of if your code returns true multiple times).


%Base Case
ancestor(Person,Ancestor):-
  parent(Ancestor,Person),
  male(Ancestor).
%Recursive Case
ancestor(Person,Ancestor):-
  parent(Parent,Person),
  male(Parent),
  ancestor(Parent,Ancestor).

same_name(Person1,Person2):-
  ancestor(Person1,Person2).
  %not someones_wife(Person2).

same_name(Person1, Person2):-
  ancestor(Person2,Person1).
  %not someones_wife(Person1).

same_name(Person1, Person2):-
  ancestor(Person1, Ancestor),
  ancestor(Person2, Ancestor).


%Write a predicate sqrt_list(NumberList, ResultList) that
%binds ResultList to the list of pairs consisting of a number and its square root, for each number in NumberList.

%sqrt_list([],[]).
%not working get_sqrt([H|T],[[H,Sqrt],SqrtRest]):-
sqrt_list([],[]).
sqrt_list([H|T],Rest):-
        Rest = [[H,Sqrt]|SqrtRest],
        Sqrt is sqrt(H),
        %SqrtOf_H is sqrt(H),
        sqrt_list(T,SqrtRest).
        %Sqrt = SqrtOf_H.

sign_runs([],[]).
sign_runs([X],[[X]]).

sign_runs([H1,H2|T],[[H1|Rest1]|Rest2]):-
  H1>=0,
  H2>=0,
  %Result = [H1|Rest],
  sign_runs([H2|T],[Rest1|Rest2]).

sign_runs([H1,H2|T],[[H1|Rest1]|Rest2]):-
  H1<0,H2<0,sign_runs([H2|T],[Rest1|Rest2]).

sign_runs([H1,H2|T],[[H1]|Rest]):-
  H1>=0,
  H2<0,
  sign_runs([H2|T],Rest).

sign_runs([H1,H2|T],[[H1]|Rest]):-
  H1<0,H2>=0,sign_runs([H2|T],Rest).


%sign_runs([H|T],[[H|T1]|Tail]):-
  %H >=0,sign_runs([T],[[H,X|T1]|Tail]).
%sign_runs([H|T],[[H|T1]|Tail]):-
  %Head<0,sign_runs([T],[[H,X|T1]|Tail]).
  %check_p(H),sign_runs(T,PList).
%sign_runs([],[]).

some_value(tree(_,Vr,_), V):-
  Vr >= V.
some_value(empty, _).
% some_value(tree(L,V,R)):-
%   R >= V,L >= V.

is_heap(empty).
is_heap(tree(L,V,R)):-
  some_value(L, V),
  some_value(R, V),
  is_heap(L),
  is_heap(R).
