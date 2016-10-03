---
title: Veterans Employment Center
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/employment/
status: normal
category: Manage
description: Saved $14M+ in vendor costs by merging 40 Veteran employment sites for just $9K in two weeks
before_jpg: vec_old.png
after_jpg: vec.png
tiles:

  - name: Development cost
    layout: savings
    datapoint: $9k
    before: $14m

  - name: Months to deliver
    layout: compare_bars
    datapoint: 1
    before: 24
    before_text: Vendor estimate
    after_text: Vets.gov actual

  - name: Maintenance marginal cost for each updated link
    layout: savings
    datapoint: $0
    before: $100k

  - name: <span class="glyphicon glyphicon-user tab-icon" aria-hidden="true"></span><span>Users</span>
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

  - name: <span class="glyphicon glyphicon-file tab-icon" aria-hidden="true"></span><span>Page views</span>
    layout: chart
    data: core_views
    context: Total page views per week
    cols:
      - id: views
        label: Count of pageviews
---
