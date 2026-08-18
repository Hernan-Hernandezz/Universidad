'use client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

const Page = () => {
  const router = useRouter();
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }
    };
    cargarDatos();
  }, []);
  return <></>;
};

export default Page;
