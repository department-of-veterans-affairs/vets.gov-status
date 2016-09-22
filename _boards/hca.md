---
title: Health Care Application
date_added: 2016-06-30 00:00:00 -0500
vetsdotgov_url: https://www.vets.gov/healthcare/apply/
status: new
category: Apply
description: Increasing online applications from 10% before to 40% in 2017
before_jpg: healthcare_old.png
after_jpg: healthcare.png
tiles:

  - name: Online applications
    layout: compare
    datapoint: 50%
    before: 10%

  - name: Mobile availability
    layout: icon
    icon: phone
    text: Veterans can now complete their application entirely from a smartphone

  - name: Automatically processed applications
    layout: compare
    datapoint: 495
    before: 62
    context: per day that require no manual intervention

  - name: <span class="glyphicon glyphicon-signal" aria-hidden="true"></span><p>Site Traffic</p>
    layout: chart
    data: hca_users
    context: Total users per week
    cols:
      - id: all
        label: Count of users

  - name: <span class="glyphicon glyphicon-phone" aria-hidden="true"></span><p>Mobile Usage</p>
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
