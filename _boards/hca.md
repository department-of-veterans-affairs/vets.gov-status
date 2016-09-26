---
title: Health Care Application
date_added: 2016-06-30 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/healthcare/apply/
status: new
category: Apply
description: Increased online submissions from 62/day to 500/day
before_jpg: healthcare_old.png
after_jpg: healthcare.png
tiles:

  - name: Cost per year
    layout: savings
    datapoint: $8k
    before: $8m

  - name: Daily online submissions
    layout: compare_bars
    datapoint: 500
    before: 62

  - name: Minutes to complete
    layout: compare
    datapoint: 12-22
    before: 45+

  - name: <span class="glyphicon glyphicon-user tab-icon" aria-hidden="true"></span><span>Users</span>
    layout: chart
    data: hca_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone tab-icon" aria-hidden="true"></span><span>Mobile Usage</span>
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
---

Only 10% of veterans apply for health care online...

...maybe because more than 70% of browsers are unable to access the application.
