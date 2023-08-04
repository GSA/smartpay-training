
const base_url = import.meta.env.PUBLIC_API_BASE_URL

export async function fetchAgencyList() {
  return fetch(`${base_url}/api/v1/agencies`).then((r) => r.json())
}
