'use client';
import { fetchAPI } from '@/app/lib/api';
import { useState, useEffect } from 'react';

const Academico = () => {
  const [resumen, setResumen] = useState([]);
  useEffect(() => {
    const cargarDatos = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }
      //llamados a la api desde el la funcion fetchAPI que hace verificacion de login
      const dataResumen = await fetchAPI('/user/academic_summary', token);
      //asigno los valores a los estados para pòsterior mente poder mostrarlos
      setResumen(dataResumen);
    };
    cargarDatos();
  }, []);
  return (
    <div>
      <h1>Resumen Académico</h1>
      <div className="grid h-fit w-max grid-cols-2 text-left">
        <p>asignatura</p>
        <p>nota</p>
        {resumen.map((r, index) => (
          <div className="col-span-2 grid grid-cols-2" key={index}>
            <p>{r.nombre_materia}</p>
            <p>Nota: {r.nota_final ?? 'Sin calificar'}</p>
            <progress max="5.0" value={r.nota_final}></progress>
            <p> {(r.nota_final / 5.0) * 100}%</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Academico;
