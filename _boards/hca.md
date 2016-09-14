---
title: Health Care Application
subtitle: Before 8% of Veterans were able to access the application
tiles:
  - name: Daily Submissions
    layout: basic
    datapoint: 750
    context: on average

  - name: Mobile availability
    layout: basic
    datapoint: 100%
    context: of content available on mobile

  - name: Fully automated
    layout: basic
    datapoint: 50%
    context: of submission

  - name: Site Traffic
    layout: chart
    data: hca_sessions
    context: Total user sessions per day
    cols:
      - id: sessions
        label: Number of Sessions

  - name: Mobile Usage
    layout: chart
    data: hca_mobile
    context: Percentage of sessions by device type
    yLabel: Percentage
    yMax: 100
    cols:
      - id: mobile
        label: Mobile
        color: rgb(17,46,81)
      - id: desktop
        label: Desktop
        color: rgb(175,175,175)

  - name: New and Returning Veterans
    layout: chart
    data: hca_new
    context: Number of users
    cols:
      - id: new
        label: New
        color: rgb(17,46,81)
      - id: returning
        label: Returning
        color: rgb(175,175,175)
---