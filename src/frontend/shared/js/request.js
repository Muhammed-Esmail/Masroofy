/**
 * Extracts the CSRF token from browser cookies.
 * Looks for a cookie named `csrftoken` and returns its value.
 * @returns {string|undefined} The CSRF token if found, otherwise undefined.
 */
function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}

/**
 * Sends a GET request to the specified URL.
 * Optionally appends query parameters to the URL.
 * @async
 * @function getRequest
 * @param {string} url - The endpoint URL.
 * @param {URLSearchParams|string} [params] - Optional query parameters.
 * @returns {Promise<any>} The parsed JSON response from the server.
 * @example
 * const data = await getRequest('/api/users', new URLSearchParams({ page: 1 }));
 */
export async function getRequest(url, params) {
    if (params) url = url+`?${params.toString()}`;
    const response = await fetch(url);
    const result = await response.json();
    return result;
}

/**
 * Sends a POST request with form data to the specified URL.
 * Automatically attaches a CSRF token in the request headers.
 * @async
 * @function postRequest
 * @param {string} url - The endpoint URL.
 * @param {Object.<string, any>} data - Key-value pairs to be sent as FormData.
 * @returns {Promise<any>} The parsed JSON response from the server.
 * @example
 * const result = await postRequest('/api/create-user', {
 *   username: 'john',
 *   email: 'john@example.com'
 * });
 */
export async function postRequest(url, data) {
    const formData = new FormData();
    for (const key in data) {
        formData.append(key, data[key]);
    }
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
    const result = await response.json();
    return result;
}

/**
 * Sends a DELETE request to the specified URL.
 * Optionally appends parameters directly to the URL path.
 * example for result url: /transaction/delete_transaction/5
 * Automatically attaches a CSRF token in the request headers.
 * @async
 * @function deleteRequest
 * @param {string} url - The endpoint URL.
 * @param {string|number} [params] - Optional identifier appended to the URL (e.g., resource ID).
 * @returns {Promise<any>} The parsed JSON response from the server.
 * @example
 * const result = await deleteRequest('/api/users/', 5);
 */
export async function deleteRequest(url, params) {
   if (params) url = url+`${params}/`;
   const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
   })
    const result = await response.json();
    return result;
}