Title: Predicting Learner Churn in MOOCs
Slug: predicting_learner_churn   
Summary: If you knew your learners were about to drop out of the awesome course you spent months working on, what would you do about it?    
Date: 2018-02-27 12:00     
Category: Projects    
Tags: Deep Learning, Churn, MOOC, Predictive Maintenance    
Authors: Kabir Khan, Software Engineer at Microsoft Worldwide Learning

> **This model was trained on data from past runs of Microsoft edX courses that are part of the [Microsoft Professional Program](https://academy.microsoft.com)**

> **If you're interested in the code for this project it's all available (for a limited time) on [Github](https://github.com/kabirkhan/edx_learner_attrition/tree/dev)**

## **Context**

On the Microsoft Worldwide Learning team we are constantly striving to provide a better experience and better content to our learners. That's why it's so important to us that learners are engaged and regularly working on and interacting with our course material. 

A few months ago, we started working on better understanding our learners' behavior, particularly around the tendency for learners to drop out and not complete courses. We decided we want to know when learners are struggling or trailing off and are likely to drop out of a course before they do.  

We settled on knowing a week in advance. We figured with this much notice, we could contact learners and attempt to re-engage them in the course, provide struggling learners with extra resources and even recommending harder courses for learners that were completing content too quickly.

---

Over the last few months, I've built a model to predict with up to 78% accuracy when learners in a course are likely to drop out a week before they do. This model was based on a few key features of learner activity, aggregated per week of each course.

### **Problem:**
Can we predict a week in advance if a learner will drop out of a course

### **Proposed solution:**
Deep learning model trained on aggregated learner activity information

## **Packages**


```python
import pandas as pd
```

## **The data**

All courses in the Microsoft Profressional Program are currently hosted on edX, a platform that does a great job collecting telemetry data on the browser and server, tied to specific learners.


```python
Example of an event collected b
```

edX cuts logs for all Microsoft courses and ships them to us where our awesome BI team injests them into our data warehouse. From there, I aggregated this learner activity information per-course per-week for each learner.

## **Data preprocessing**


```python
features = pd.DataFrame([
    {'user_id': 9999, 'course_week': 4, 'user_started_week': 3, 
     'num_video_plays': 12, 'num_subsections_viewed': 23, 
     'num_problems_attempted': 8, 'num_problems_correct': 5, 
     'num_forum_posts': 1., 'num_forum_up_votes': 3, 
     'avg_forum_sentiment': .72},
    {'user_id': 100001, 'course_week': 4, 'user_started_week': 0, 
     'num_video_plays': 0, 'num_subsections_viewed': 0, 
     'num_problems_attempted': 0, 'num_problems_correct': 0, 
     'num_forum_posts': 0, 'num_forum_up_votes': 0, 
     'avg_forum_sentiment': 0},
])

features[[
    'user_id', 'course_week', 'user_started_week', 'num_video_plays',
    'num_subsections_viewed', 'num_problems_attempted', 'num_problems_correct',
    'num_forum_posts', 'num_forum_up_votes', 'avg_forum_sentiment'
]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>user_id</th>
      <th>course_week</th>
      <th>user_started_week</th>
      <th>num_video_plays</th>
      <th>num_subsections_viewed</th>
      <th>num_problems_attempted</th>
      <th>num_problems_correct</th>
      <th>num_forum_posts</th>
      <th>num_forum_up_votes</th>
      <th>avg_forum_sentiment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9999</td>
      <td>4</td>
      <td>3</td>
      <td>12</td>
      <td>23</td>
      <td>8</td>
      <td>5</td>
      <td>1.0</td>
      <td>3</td>
      <td>0.72</td>
    </tr>
    <tr>
      <th>1</th>
      <td>100001</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
</div>


