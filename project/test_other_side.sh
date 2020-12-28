#!/bin/bash
set -eoux pipefail
test_other_side() {
  sudo python2 ./src/run_mininet.py single 3
}
main() {
  test_other_side
}
main
