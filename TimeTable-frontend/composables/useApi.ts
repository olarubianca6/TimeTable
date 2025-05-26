/**
 * Asynchronous function for making API requests with optional parameters.
 *
 * @param {string} request - the API endpoint to make the request to
 * @param {Partial<Parameters<typeof $fetch<T>>[1]>} opts - optional parameters for the request
 * @return {Promise<T | U | undefined>} a promise that resolves to the response data or undefined
 */
export default async function useApi<T, U>(
  request: string,
  opts: Partial<Parameters<typeof $fetch<T>>[1]>,
): Promise<T | U | undefined> {
  const config = useRuntimeConfig();

  // Aserții defensive
  assert(typeof request === "string" && request.length > 0, "API request path must be a non-empty string");
  assert(typeof config.public.apiUrl === "string" && config.public.apiUrl.length > 0, "Base API URL is missing in runtime config");

  const headers = {
    ...opts?.headers,
  };

  try {
    return await $fetch<T>(request, {
      baseURL: config.public.apiUrl,
      ...opts,
      headers,
    });
  } catch (error: any) {
    throw error?.data?.message ?? "Something went wrong";
  }
}