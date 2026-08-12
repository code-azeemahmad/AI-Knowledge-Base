import { useState, useEffect } from 'react';
import { getHealthStatus } from '../api/health';

export function useHealth() {
  const [status, setStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    let isMounted = true;

    async function check() {
      try {
        const res = await getHealthStatus();
        if (isMounted) {
          setStatus(res && res.status ? 'online' : 'offline');
        }
      } catch (err) {
        if (isMounted) {
          setStatus('offline');
        }
      }
    }

    check();
    const interval = setInterval(check, 15000); // Check every 15s

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return status;
}
