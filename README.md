# scheduler-actions
This project demonstrate how to use Github Actions to run a simple data gathering task and commit <code>.json</code> to a repository .

The entire project concept and code is heavily based on https://lost-stats.github.io/Other/task_scheduling_with_github_actions.html
<code>Python</code> is used in this example and it is scheduled to run everyday at 23:00:00 UTC or 07:00:00 SGP time. 
For more actions details please refer <code>pull-spx.yml</code>

# Remark
You might ignore <code>process_table(_html: str)</code> and <code>get_spx_data()</code> function in <code>main.py</code> as both are mainly use to process the http content. 
