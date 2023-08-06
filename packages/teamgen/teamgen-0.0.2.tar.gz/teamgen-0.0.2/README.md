# Tennis Team Generator

This is a pretty basic generator that takes a list of players, and generates
teams that try and make for a fairly even distribution of player skills 
on both sides of the net. It aims for the best groups.

Each player is described in a a json file, and their rating includes their USTA
rating, as well as a "Micro NTRP", that is an assessment, in 0.1 or 0.01 increments
of that actual level of play, to be more precise than the NTRP. Someone has to make
a judgement there of course, usually the group captain.

The project uses a sequence of 'random' selections, and then trows out those that fail
some criteria. 

To be frank, the algorithm isn't that great, but until I can figure out how to make a better
one, this one does the trick for me. It often requires that I run it several times, and I need
to manually review the results. Lots of room for improvement!!

## Number of Courts
The number of courts is configurable, so anywhere from 2-4 courts works.

## Number of players
You need enough players to keep the courts even, so 16 for 4 courts, etc. This does not handle singles.

## Distribution of Men and Women.
Generally, we want even numbers of men and women, but the algorithm does compensate if there are uneven
counts. 
For example, if there are 4 courts, and we have 10men and 6 women, we can do 3 courts of mixed doubles,
and one court of men's singles each round. The same applies if we have 10women and 6 men -- one court of
women's singles per round.

## Quality Metics
I have some quality metrics that "weight" the requirement of how close the players are that play together,

    I.E. Can a 4.5 play with a 3.0? That is a spread of 1.5 on one side of the court

Also, the weight of the combined rating of players across the net

    If a 4.5 and 4.0 are on one side, and a 3.5 and 4.0 on the other, that is 8.5 versus 7.5, for a spread of 1.0

## Maximum spread

We can limit the maximum spread on each court side so that we avoid a 4.5 playing with a 3.0, for example.

