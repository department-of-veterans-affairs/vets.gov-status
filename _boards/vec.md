---
title: Veterans Employment Center
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/employment/
status: normal
category: Manage
description: Will enable Veterans to verify their military status online!
tiles:

  - name: User Experience
    layout: image-compare
    before: old-healthcare.jpg
    after: healthcare.jpg

  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Mobile availability
    layout: icon
    icon: smartphone.svg
    text: Veterans can now complete their application entirely from a smartphone    

  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Site Traffic
    layout: chart
    data: vec_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: Mobile Usage
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

  - name: New and Returning Users
    layout: chart
    data: vec_new
    context: Count of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---
