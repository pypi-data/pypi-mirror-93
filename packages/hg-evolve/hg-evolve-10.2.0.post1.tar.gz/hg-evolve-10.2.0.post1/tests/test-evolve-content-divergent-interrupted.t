=======================================================
Tests the resolution of content divergence: interrupted
=======================================================

This file intend to cover case where evolve has to be interrupted.

This test aims at gather test case for --abort, --continue and --stop


Tests for the --abort flag for `hg evolve` command while content-divergence resolution
======================================================================================

The `--abort` flag aborts the interrupted evolve by undoing all the work which
was done during resolution i.e. stripping new changesets created, moving
bookmarks back, moving working directory back.

This test contains cases when `hg evolve` is doing content-divergence resolution.

Setup
=====

  $ cat >> $HGRCPATH <<EOF
  > [phases]
  > publish = False
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc}\n ({bookmarks}) {phase}"
  > [experimental]
  > evolution.allowdivergence = True
  > [extensions]
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

  $ hg init abortrepo
  $ cd abortrepo
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Creating content divergence, resolution of which will lead to conflicts
-----------------------------------------------------------------------

  $ echo bar > d
  $ hg amend

  $ hg up c41c793e0ef1 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset c41c793e0ef1
  (hidden revision 'c41c793e0ef1' was rewritten as: e49523854bc8)
  working directory parent is obsolete! (c41c793e0ef1)
  (use 'hg evolve' to update to its successor: e49523854bc8)

  $ echo foobar > d
  $ hg amend
  2 new content-divergent changesets
  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent --no-all
  merge:[6] added d
  with: [5] added d
  base: [4] added d
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg status -v
  M d
  # The repository is in an unfinished *evolve* state.
  
  # Unresolved merge conflicts:
  # 
  #     d
  # 
  # To mark files as resolved:  hg resolve --mark FILE
  
  # To continue:    hg evolve --continue
  # To abort:       hg evolve --abort
  # To stop:        hg evolve --stop
  # (also see `hg help evolve.interrupted`)
  
  $ hg parents
  changeset:   6:9c1631e352d9
  tag:         tip
  parent:      3:ca1b80f7960a
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  instability: content-divergent
  summary:     added d
  
  changeset:   5:e49523854bc8
  parent:      3:ca1b80f7960a
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  instability: content-divergent
  summary:     added d
  

  $ hg evolve --abort
  evolve aborted
  working directory is now at 9c1631e352d9

  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Creating multiple content-divergence where resolution of last one results in
conflicts and resolution of first one resulted in no new commit
-----------------------------------------------------------------------------

  $ echo watbar > d
  $ hg amend
  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bar > c
  $ hg amend
  2 new orphan changesets
  $ hg up ca1b80f7960a --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory parent is obsolete! (ca1b80f7960a)
  (use 'hg evolve' to update to its successor: 2ba73e31f264)
  $ echo foobar > c
  $ hg amend
  2 new content-divergent changesets
  $ echo bar > c
  $ hg amend

  $ hg glog --hidden
  @  10:491e10505bae added c
  |   () draft
  | x  9:7398f702a162 added c
  |/    () draft
  | *  8:2ba73e31f264 added c
  |/    () draft
  | *  7:f0f1694f123e added d
  | |   () draft
  | | x  6:9c1631e352d9 added d
  | |/    () draft
  | | *  5:e49523854bc8 added d
  | |/    () draft
  | | x  4:c41c793e0ef1 added d
  | |/    () draft
  | x  3:ca1b80f7960a added c
  |/    () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --all --content-divergent
  merge:[8] added c
  with: [10] added c
  base: [3] added c
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[5] added d
  with: [7] added d
  base: [4] added d
  rebasing "divergent" content-divergent changeset e49523854bc8 on 4566502c0483
  rebasing "other" content-divergent changeset f0f1694f123e on 4566502c0483
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg evolve --abort
  2 new orphan changesets
  2 new content-divergent changesets
  evolve aborted
  working directory is now at 491e10505bae

  $ hg glog --hidden
  @  10:491e10505bae added c
  |   () draft
  | x  9:7398f702a162 added c
  |/    () draft
  | *  8:2ba73e31f264 added c
  |/    () draft
  | *  7:f0f1694f123e added d
  | |   () draft
  | | x  6:9c1631e352d9 added d
  | |/    () draft
  | | *  5:e49523854bc8 added d
  | |/    () draft
  | | x  4:c41c793e0ef1 added d
  | |/    () draft
  | x  3:ca1b80f7960a added c
  |/    () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg obslog -r . --all
  *  2ba73e31f264 (8) added c
  |    amended(content) from ca1b80f7960a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  | @  491e10505bae (10) added c
  | |    amended(content) from 7398f702a162 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  7398f702a162 (9) added c
  |/     amended(content) from ca1b80f7960a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  ca1b80f7960a (3) added c
  
  $ cd ..

Creating content-divergence on multiple parents when gca of divergent changesets
is parent of one of the divergents and relocating leads to conflicts
---------------------------------------------------------------------------------

  $ hg init multiparent
  $ cd multiparent
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg rebase -r . -d .^^^ --config extensions.rebase=
  rebasing 4:c41c793e0ef1 tip "added d"
  $ echo bar > c
  $ hg add c
  $ hg amend

  $ hg up --hidden 'min(desc("added d"))'
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset c41c793e0ef1
  (hidden revision 'c41c793e0ef1' was rewritten as: 69bdd23a9b0d)
  working directory parent is obsolete! (c41c793e0ef1)
  (use 'hg evolve' to update to its successor: 69bdd23a9b0d)
  $ echo bar > d
  $ hg amend
  2 new content-divergent changesets

  $ hg glog
  @  7:e49523854bc8 added d
  |   () draft
  | *  6:69bdd23a9b0d added d
  | |   () draft
  o |  3:ca1b80f7960a added c
  | |   () draft
  o |  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[6] added d
  with: [7] added d
  base: [4] added d
  rebasing "other" content-divergent changeset e49523854bc8 on c7586e2a9264
  file 'c' was deleted in other but was modified in local.
  You can use (c)hanged version, (d)elete, or leave (u)nresolved.
  What do you want to do? u
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg evolve --abort
  evolve aborted
  working directory is now at e49523854bc8

  $ hg glog
  @  7:e49523854bc8 added d
  |   () draft
  | *  6:69bdd23a9b0d added d
  | |   () draft
  o |  3:ca1b80f7960a added c
  | |   () draft
  o |  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Creating content-divergence on multiple parents when gca of divergent changesets
is parent of one of the divergents and merging divergent leads to conflicts
---------------------------------------------------------------------------------

  $ hg up 'min(desc("added d"))'
  2 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg rm c
  $ echo wat > d
  $ hg amend

  $ hg glog
  @  8:33e4442acf98 added d
  |   () draft
  | *  7:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[7] added d
  with: [8] added d
  base: [4] added d
  rebasing "divergent" content-divergent changeset e49523854bc8 on c7586e2a9264
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg evolve --abort
  evolve aborted
  working directory is now at 33e4442acf98

  $ hg glog
  @  8:33e4442acf98 added d
  |   () draft
  | *  7:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft
  $ cd ..

Tests for the --stop flag for `hg evolve` command while resolving content-divergence
==================================================================================

The `--stop` flag stops the interrupted evolution and delete the state file so
user can do other things and comeback and do evolution later on

This is testing cases when `hg evolve` command is doing content-divergence resolution.

Setup
=====

  $ hg init stoprepo
  $ cd stoprepo
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Creating content divergence, resolution of which will lead to conflicts
-----------------------------------------------------------------------

  $ echo bar > d
  $ hg amend

  $ hg up 'min(desc("added d"))' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset c41c793e0ef1
  (hidden revision 'c41c793e0ef1' was rewritten as: e49523854bc8)
  working directory parent is obsolete! (c41c793e0ef1)
  (use 'hg evolve' to update to its successor: e49523854bc8)

  $ echo foobar > d
  $ hg amend
  2 new content-divergent changesets
  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent --no-all
  merge:[6] added d
  with: [5] added d
  base: [4] added d
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at 9c1631e352d9

  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Content divergence with parent change which will result in conflicts while
merging
---------------------------------------------------------------------------

  $ hg rebase -r . -d .^^^ --config extensions.rebase=
  rebasing 6:9c1631e352d9 tip "added d"

  $ hg glog
  @  7:517d4375cb72 added d
  |   () draft
  | *  5:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[5] added d
  with: [7] added d
  base: [4] added d
  rebasing "divergent" content-divergent changeset e49523854bc8 on c7586e2a9264
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at e49523854bc8

  $ hg glog
  *  7:517d4375cb72 added d
  |   () draft
  | @  5:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Content-divergence with parent-change which will result in conflicts while
relocation
---------------------------------------------------------------------------

  $ echo babar > c
  $ hg add c
  c already tracked!
  $ hg amend
  $ hg glog
  @  8:2d664a4ab749 added d
  |   () draft
  | *  7:517d4375cb72 added d
  | |   () draft
  o |  3:ca1b80f7960a added c
  | |   () draft
  o |  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[7] added d
  with: [8] added d
  base: [4] added d
  rebasing "other" content-divergent changeset 2d664a4ab749 on c7586e2a9264
  file 'c' was deleted in local but was modified in other.
  You can use (c)hanged version, leave (d)eleted, or leave (u)nresolved.
  What do you want to do? u
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 2 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]

  $ hg diff
  diff -r 517d4375cb72 c
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +babar
  diff -r 517d4375cb72 d
  --- a/d	Thu Jan 01 00:00:00 1970 +0000
  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< local: 517d4375cb72 - test: added d
   foobar
  +=======
  +bar
  +>>>>>>> other: e315463d94bd - test: added d

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at 2d664a4ab749

XXX: we should have preserved the wdir to be at rev 8
  $ hg glog
  @  8:2d664a4ab749 added d
  |   () draft
  | *  7:517d4375cb72 added d
  | |   () draft
  o |  3:ca1b80f7960a added c
  | |   () draft
  o |  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft
  $ cd ..
