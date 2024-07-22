document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('tasks');

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const newTaskInput = document.getElementById('new-task');
        const taskTimeInput = document.getElementById('task-time');
        const recurringInput = document.getElementById('recurring');
        const taskText = newTaskInput.value.trim();
        const taskTime = taskTimeInput.value;
        const recurring = recurringInput.value;

        if (taskText === '' || taskTime === '') {
            return;
        }

        addTask(taskText, taskTime, recurring);

        newTaskInput.value = '';
        taskTimeInput.value = '';
        recurringInput.value = 'none';
    });

    function addTask(text, time, recurring) {
        const taskItem = document.createElement('li');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        taskItem.appendChild(checkbox);

        const label = document.createElement('label');
        label.textContent = text;
        taskItem.appendChild(label);

        const timeLabel = document.createElement('span');
        timeLabel.className = 'task-time';
        timeLabel.textContent = `Due: ${new Date(time).toLocaleString()}`;
        taskItem.appendChild(timeLabel);

        const recurringLabel = document.createElement('span');
        recurringLabel.className = 'recurring';
        if (recurring !== 'none') {
            recurringLabel.textContent = ` (Recurring: ${recurring})`;
        }
        taskItem.appendChild(recurringLabel);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'delete-btn';
        deleteButton.addEventListener('click', function() {
            taskList.removeChild(taskItem);
        });
        taskItem.appendChild(deleteButton);

        taskList.appendChild(taskItem);

        if (recurring !== 'none') {
            setRecurringTask(text, time, recurring);
        }
    }

    function setRecurringTask(text, time, recurring) {
        const interval = getRecurringInterval(recurring);

        setInterval(function() {
            const newTime = new Date(time);
            newTime.setTime(newTime.getTime() + interval);
            addTask(text, newTime.toISOString(), recurring);
        }, interval);
    }

    function getRecurringInterval(recurring) {
        const dayInMilliseconds = 24 * 60 * 60 * 1000;
        switch (recurring) {
            case 'daily':
                return dayInMilliseconds;
            case 'weekly':
                return 7 * dayInMilliseconds;
            case 'monthly':
                return 30 * dayInMilliseconds;
            default:
                return 0;
        }
    }
});