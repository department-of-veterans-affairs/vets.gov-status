#!/usr/bin/env bash
docker run --rm -p 4000:4000 --volume=${PWD}:/srv/jekyll -it jekyll/jekyll:4.0  jekyll serve
