---
title: Veterans Employment Center
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/employment/
status: normal
category: Manage
description: Will enable Veterans to verify their military status online!
before_jpg: vec_old.png
after_jpg: vec.png
tiles:

  - name: Savings
    layout: basic
    datapoint: $8m
    context: using small, agile teams

  - name: Mobile availability
    layout: icon
    icon: phone
    text: Enables Veterans to find employment opportunities on their mobile devices   

  - name: <span class="glyphicon glyphicon-signal" aria-hidden="true"></span><p>Site Traffic</p>
    layout: chart
    data: vec_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone" aria-hidden="true"></span><p>Mobile Usage</p>
    layout: chart
    data: vec_mobile
    context: Percentage of users by device type used
    yLabel: Percentage
    yMax: 100
    cols:
      - id: mobile
        label: Mobile
        color: rgb(17,46,81)
      - id: desktop
        label: Desktop
        color: rgb(175,175,175)
---
