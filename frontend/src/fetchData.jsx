import { useState, useEffect } from 'react';

export const useFetch = (url, method = 'GET', bodyData = null) => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [apiError, setApiError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: bodyData ? JSON.stringify(bodyData) : null
                });
                console.log(response)
                const result = await response.json();
                
                // Check if the result contains the error field
                if (result.error) {
                    setApiError(result.error);
                } else {
                    setData(result);
                }
                
            } catch (err) {
                setError(err);
            }
        };
        fetchData();
    }, [url, method, bodyData]);

    return { data, error, apiError };
}

export default useFetch;