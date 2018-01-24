# TODO and misc. thoughts

## reimplementing core functionality
The original implementation of AMSAF functionality (in AmsafExecutor.py)
is needlessly stateful, complex, and relies on a few large functions with
many side effects. This has made testing difficult, refactoring scary,
and collaboration painful.

Ian is currently reimplementing AMSAF functionality in a way influenced
by functional programming concepts. The end result should consist of
nearly stateless, mostly pure, small, and composable functions. Conequently,
testing will be easier and faster and performance will be more predictable
with the potential for big speedups in the future if distributed computing
comes into play. In addition, general code complexity and verbosity should
be greatly reduced, making collaboration and refactoring much cleaner.

## better testing and parameter map refinement
AMSAF's main roadblock to progress is the problem of there being no easy
way to productively gauge results and make improvements. The HART lab team
responsible for its development typically meets weekly and looks at some
results before suggesting  minor changes to parameter map combinations.
As a result, progress has slowed to a halt.

Barring a complete machine learning-themed overhaul, the best way to improve
this workflow will be to make it easier for team members to view and rate
AMSAF results. 

Ian proposes that we accomplish this by developing a script that can email
team members with screenshots of top results, and possibly allow members
to respond with a rating which will influence future AMSAF iterations.

Alternatively, a better long-term solution might be to develop a small web
application which allows users to see top results, run or stop AMSAF
execution, and possibly edit parameter maps.

