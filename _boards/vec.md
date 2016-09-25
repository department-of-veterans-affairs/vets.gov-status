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

  - name: Cost
    layout: savings
    datapoint: $6k
    before: $24m

  - name: Mobile availability
    layout: icon
    icon: phone
    text: Enables Veterans to find employment opportunities on their mobile devices   

  - name: Months to deliver
    layout: compare_bars
    datapoint: 1
    before: 12

  - name: <span class="glyphicon glyphicon-signal tab-icon" aria-hidden="true"></span><span>Site Traffic</span>
    layout: chart
    data: vec_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone tab-icon" aria-hidden="true"></span><span>Mobile Usage</span>
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
