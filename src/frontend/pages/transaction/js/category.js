import { API } from '/static/api/API.js';

const api = new API();
api.setBase('/transaction');

async function addCategory(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());
    const response = await api.request('/add_category/', 'POST', data);
    if (response.success) {
        alert('Category created!');
    } else {
        alert('Failed: ' + JSON.stringify(response));
    }
}

async function updateCategory(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());
    const response = await api.request('/update_category/', 'POST', data);
    if (response.success) {
        alert('Category updated!');
    } else {
        alert('Failed: ' + JSON.stringify(response));
    }
}

async function deleteCategory() {
    const name = document.querySelector('#delete-category-form select[name="name"]').value;
    const response = await api.request(`/delete_category/${name}/`, 'DELETE');
    if (response.success) {
        alert('Category deleted!');
    } else {
        alert('Failed: ' + JSON.stringify(response));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('add-category-form').addEventListener('submit', addCategory);
    document.getElementById('update-category-form').addEventListener('submit', updateCategory);
    document.getElementById('delete-category-form').addEventListener('submit', deleteCategory);
});