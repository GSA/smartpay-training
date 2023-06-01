
// const base_url = import.meta.env.PUBLIC_API_BASE_URL

const tempAgencies = [
  { 'id': 1, 'name': 'GSA', 'bureaus': []},
  { 'id': 2, 
    'name': 'Department of the Treasury', 
    'bureaus': [
      {'id': 3, 'name': 'United States Mint'},
      {'id': 4, 'name': 'Financial Crimes Enforcement'}
    ]
  },
  { 'id': 5, 'name': 'Department of the Interior', 'bureaus': []}
]

export async function fetchAgencyList() {
  //return fetch(`${base_url}/api/v1/agencies`).then((r) => r.json())
  return Promise.resolve(tempAgencies)
}
