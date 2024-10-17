import { describe, beforeEach, it, expect, vi} from 'vitest'
import AdminRepository from '../AdminRepository.vue'
import { profile } from '../../stores/user.js'
import { useStore } from '@nanostores/vue'

describe('AdminRepository', async () => {
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
  const user = useStore(profile)

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('should successfully download the report', async () => {
    const mockResponse = new Response('mocked report content', {
      status: 200,
      headers: { 'Content-Type': 'text/csv' },
    });

    // Mock the fetch function
    global.fetch = vi.fn().mockResolvedValue(mockResponse);

    const filterData = { }; // sample filter data
    const result = await AdminRepository.downloadTrainingReport(filterData);

    expect(fetch).toHaveBeenCalledWith(`${base_url}/api/v1/users/download-admin-smartpay-training-report`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${user.value.jwt}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filterData),
    });
    expect(result).toBe(mockResponse); // Check if the raw response is returned
  });

  it('should throw an error when response is not ok', async () => {
    const mockErrorMessage = 'Error occurred';
    const mockErrorResponse = new Response(mockErrorMessage, { status: 400 });

    // Mock the fetch function to return an error response
    global.fetch = vi.fn().mockResolvedValue(mockErrorResponse);

    const filterData = { quizId: 123 };

    await expect(AdminRepository.downloadTrainingReport(filterData)).rejects.toThrow(mockErrorMessage);
    expect(fetch).toHaveBeenCalled();
  });
});