#!/bin/bash
set -eoux pipefail
test_one_side() {
  ryu-manager --observe-links ./src/shortest_paths.py
}
main() {
  test_one_side
}
main
