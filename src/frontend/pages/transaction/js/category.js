import { API } from '/static/api/API.js';

const api = new API();
api.setBase('/transaction');

async function addCategory(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target).entries());
    const response = await api.request('/add_category/', 'POST', data);
    console.log(response)
    if (response.ok) {
        alert('Category created!');
        window.location.reload();

    } else {
        alert('Failed: ' + response.description);
    }
}

async function updateCategory(e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target).entries());
    const response = await api.request('/update_category/', 'POST', data);
    if (response.ok) {
        alert('Category updated!');
        window.location.reload();
    } else {
        alert('Failed: ' + response.description);
    }
}

async function deleteCategory(e) {
    e.preventDefault();

    const name = document.querySelector('#delete-category-form select[name="name"]').value;
    const response = await api.request(`/delete_category/${name}/`, 'DELETE');
    if (response.ok) {
        alert('Category deleted!');
        window.location.reload();
    } else {
        alert('Failed: ' + response.description);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('add-category-form').addEventListener('submit', addCategory);
    document.getElementById('update-category-form').addEventListener('submit', updateCategory);
    document.getElementById('delete-category-form').addEventListener('submit', deleteCategory);
});