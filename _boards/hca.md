---
title: Health Care Application
date_added: 2016-06-30 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/healthcare/apply/
status: normal
category: Apply
description: Increased online submissions from 62/day to 500/day
before_jpg: healthcare_old.png
after_jpg: healthcare.png
tiles:

  - name: Daily online submissions
    layout: compare_bars
    id: submissions
    datapoint: 500
    before: 62
    before_text: Veteran Online Application

  - name: Online applications submitted
    layout: basic
    datapoint: "50,797"
    context: since launch

  - name: Online portion of 582k annual healthcare applications
    layout: compare_pie
    id: applications
    datapoint: 50
    before: 10
    after_text: 2017

  - name: <span class="glyphicon glyphicon-user tab-icon" aria-hidden="true"></span><span>Users</span>
    layout: chart
    data: hca_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone tab-icon" aria-hidden="true"></span><span>Mobile Use</span>
    layout: chart
    data: hca_mobile
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

  - name: <span class="glyphicon glyphicon-file tab-icon" aria-hidden="true"></span><span>Views</span>
    layout: chart
    data: hca_views
    context: Total page views per week
    cols:
      - id: views
        label: Count of pageviews
---
