document.addEventListener("DOMContentLoaded", () => {
    const visitRecords = document.getElementById("visit-records");
    const nextAppointmentTime = document.getElementById("next-appointment-time");
    const reminders = document.getElementById("reminders");
    const patientName = document.getElementById("patient-name");

    // Fetch patient data from API
    fetch('/api/patients')
        .then(response => response.json())
        .then(patient => {
            patientName.textContent = patient.name; // Update patient name in the DOM

            // Fetch recent visits
            fetch(`/api/medical_records/${patient.id}`)
                .then(response => response.json())
                .then(records => {
                    if (records.length > 0) {
                        visitRecords.innerHTML = ''; // Clear previous content
                        records.forEach(record => {
                            const visitElement = document.createElement("p");
                            visitElement.textContent = `日期：${record.record_date}，記錄：${record.record}`;
                            visitRecords.appendChild(visitElement);
                        });
                        // Example: Set next appointment time based on the latest record
                        nextAppointmentTime.textContent = `下一次回診時間：${records[0].record_date} 10:00`;
                    } else {
                        visitRecords.textContent = "無";
                    }
                })
                .catch(error => {
                    console.error('Error fetching medical records:', error);
                });

            // Fetch health reminders
            fetch(`/api/health_reminders/${patient.id}`)
                .then(response => response.json())
                .then(remindersData => {
                    if (remindersData.length > 0) {
                        reminders.innerHTML = ''; // Clear previous content
                        remindersData.forEach(reminder => {
                            const reminderElement = document.createElement("p");
                            reminderElement.textContent = reminder.reminder;
                            reminders.appendChild(reminderElement);
                        });
                    } else {
                        reminders.textContent = "無健康提醒";
                    }
                })
                .catch(error => {
                    console.error('Error fetching health reminders:', error);
                });
        })
        .catch(error => {
            console.error('Error fetching patient data:', error);
        });
});
