let editMode = false;
let academicTable, experienceTable;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function toggleEditMode() {
    editMode = !editMode;
    const editButton = document.querySelector('.btn-edit');
    editButton.innerHTML = editMode ? '<i class="fas fa-save"></i> Save' : '<i class="fas fa-edit"></i> Edit';

    document.querySelectorAll('.info-value').forEach(span => {
        span.style.display = editMode ? 'none' : 'inline';
    });

    document.querySelectorAll('.info-item input, .info-item textarea').forEach(input => {
        input.style.display = editMode ? 'block' : 'none';
        if (!editMode) {
            input.previousElementSibling.textContent = input.value;
        }
    });

    const tables = [academicTable, experienceTable];
    tables.forEach(table => {
        table.columns().every(function() {
            const column = this;
            const cells = column.nodes().to$();
            if (editMode) {
                cells.attr('contenteditable', true);
            } else {
                cells.attr('contenteditable', false);
                table.draw(false);
            }
        });
    });

    const addButtons = document.querySelectorAll('.btn-add');
    addButtons.forEach(button => {
        button.style.display = editMode ? 'inline-block' : 'none';
    });

    if (editMode) {
        addTableButtons();
    } else {
        saveProfile();
        const addButtons = document.querySelectorAll('.btn-add');
        addButtons.forEach(button => button.remove());
    }
}

function addTableButtons() {
    const academicSection = document.getElementById('academicInfo');
    const experienceSection = document.getElementById('experiences');

    const addAcademicButton = document.createElement('button');
    addAcademicButton.className = 'btn btn-primary mt-3 btn-add';
    addAcademicButton.innerHTML = '<i class="fas fa-plus"></i> Add Academic Record';
    addAcademicButton.onclick = () => addTableRow('academicTable');

    const addExperienceButton = document.createElement('button');
    addExperienceButton.className = 'btn btn-primary mt-3 btn-add';
    addExperienceButton.innerHTML = '<i class="fas fa-plus"></i> Add Experience';
    addExperienceButton.onclick = () => addTableRow('experienceTable');

    academicSection.appendChild(addAcademicButton);
    experienceSection.appendChild(addExperienceButton);
}

function addTableRow(tableId) {
    const table = tableId === 'academicTable' ? academicTable : experienceTable;
    const rowData = tableId === 'academicTable' 
        ? ['New Degree', 'Institution', 'Grade', 'Year']
        : ['New Position', 'Organization', 'Start Date', 'End Date'];
    table.row.add(rowData).draw(false);
}

function saveProfile() {
    const formData = new FormData();
    document.querySelectorAll('.info-item input, .info-item textarea').forEach(input => {
        formData.append(input.name, input.value);
    });

    fetch('/brothers_profile/update/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Profile updated successfully');
        } else {
            alert('Error updating profile');
        }
    });

    saveAcademicRecords();
    saveExperiences();
    saveSocialLinks();
}

function saveAcademicRecords() {
    const records = academicTable.rows().data().toArray();

    fetch('/brothers_profile/clear_academic_records/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(() => {
        records.forEach(record => {
            const formData = new FormData();
            formData.append('degree', record[0]);
            formData.append('institution', record[1]);
            formData.append('grade', record[2]);
            formData.append('year', record[3]);

            fetch('/brothers_profile/add_academic_record/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
        });
    });
}

function saveExperiences() {
    const experiences = experienceTable.rows().data().toArray();
    experiences.forEach(experience => {
        const formData = new FormData();
        formData.append('position', experience[0]);
        formData.append('organization', experience[1]);
        formData.append('start_date', experience[2]);
        formData.append('end_date', experience[3]);

        fetch('/brothers_profile/add_experience/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
    });
}

function saveSocialLinks() {
    const formData = new FormData();
    document.querySelectorAll('.social-links a').forEach(link => {
        formData.append(`social_${link.classList[1].replace('fa-', '')}`, link.href);
    });

    fetch('/brothers_profile/update_social_links/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
}

function updateProfilePicture(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profilePic').src = e.target.result;
        };
        reader.readAsDataURL(file);

        const formData = new FormData();
        formData.append('profile_picture', file);

        fetch('/brothers_profile/update/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        });
    }
}

function exportToPDF() {
    alert('Exporting to PDF... (This is a placeholder for the actual PDF export functionality)');
    // Implement actual PDF export logic here
}

// Initialize DataTables and set up event listeners
$(document).ready(function() {
    academicTable = $('#academicTable').DataTable({
        paging: true,
        searching: false,
        info: false,
        lengthChange: false
    });

    experienceTable = $('#experienceTable').DataTable({
        paging: true,
        searching: false,
        info: false,
        lengthChange: false
    });

    document.getElementById('profilePicEdit').addEventListener('click', function() {
        if (editMode) {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = updateProfilePicture;
            input.click();
        }
    });

    document.getElementById('profileTitle').addEventListener('click', function() {
        if (editMode) {
            const currentTitle = this.textContent;
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentTitle;
            input.className = 'form-control';
            
            input.onblur = function() {
                document.getElementById('profileTitle').textContent = this.value;
                this.remove();
            };

            this.textContent = '';
            this.appendChild(input);
            input.focus();
        }
    });

    // Ajax functionality for form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const url = form.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    });
});