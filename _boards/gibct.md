---
title: GI Bill Comparison Tool
date_added: 2015-11-01 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/gi-bill-comparison-tool/
status: normal
category: Discover
description: Includes school performance data--and caution flags to warn Veterans
before_jpg: gibct_old.png
after_jpg: gibct.png
tiles:

  - name: Real-time caution warnings
    layout: icon
    icon: warning-sign
    text: Warns on schools that are not performing well immediately

  - name: Days in release cycle
    layout: compare_bars
    before: 90
    datapoint: 7

  - name: <span class="glyphicon glyphicon-user tab-icon" aria-hidden="true"></span><span>Users</span>
    layout: chart
    data: gibct_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone tab-icon" aria-hidden="true"></span><span>Mobile Usage</span>
    layout: chart
    data: gibct_mobile
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
