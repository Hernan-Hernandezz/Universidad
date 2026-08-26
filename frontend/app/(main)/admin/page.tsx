'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { fetchAPI, putAPI, postAPI, deleteAPI } from '../../lib/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// ─── Tipos ────────────────────────────────────────────────────
type Usuario = { id_usuario: number; nombre: string; correo: string; activo: boolean; rol: string };
type Asignatura = {
  id_asignatura: number;
  codigo: string;
  nombre_materia: string;
  creditos: number;
};
type Clase = {
  id_clase: number;
  nombre_materia: string;
  docente: string;
  periodo_academico: string;
  grupo: string;
};

// ─── Componente principal ─────────────────────────────────────
export default function AdminPanel() {
  const router = useRouter();
  const [tab, setTab] = useState<'usuarios' | 'asignaturas' | 'clases' | 'alertas'>('usuarios');
  const [token, setToken] = useState('');

  // datos
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [clases, setClases] = useState<Clase[]>([]);

  // formularios
  const [nuevoUsuario, setNuevoUsuario] = useState({
    nombre: '',
    correo: '',
    contrasena: '',
    id_rol: 1,
  });
  const [nuevaAsignatura, setNuevaAsignatura] = useState({
    codigo: '',
    nombre_materia: '',
    creditos: 3,
  });
  const [nuevaClase, setNuevaClase] = useState({
    id_asignatura: 0,
    id_docente: 0,
    periodo_academico: '2026-1',
    grupo: '01',
    cupo_maximo: 35,
  });
  const [nuevaAlerta, setNuevaAlerta] = useState({
    titulo: '',
    mensaje: '',
    prioridad: 'Media',
    id_creador: 0,
  });
  const [msg, setMsg] = useState('');

  useEffect(() => {
    const t = localStorage.getItem('token');
    if (!t) {
      router.push('/login');
      return;
    }
    setToken(t);
    cargarDatos(t);
  }, []);

  const cargarDatos = async (t: string) => {
    const [u, a, c] = await Promise.all([
      fetchAPI('/admin/usuarios/lista', t),
      fetchAPI('/admin/asignaturas/lista', t),
      fetchAPI('/admin/clases/lista', t),
    ]);
    console.log('usuarios:', u); // ← agrega esto
    console.log('asignaturas:', a);
    console.log('clases:', c);
    setUsuarios(u || []);
    setAsignaturas(a || []);
    setClases(c || []);
  };

  const mostrarMsg = (m: string) => {
    setMsg(m);
    setTimeout(() => setMsg(''), 3000);
  };

  // ─── Acciones ──────────────────────────────────────────────
  const crearUsuario = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await postAPI('/admin/usuarios', nuevoUsuario, token);
    mostrarMsg(res.mensaje || 'Error al crear usuario');
    cargarDatos(token);
    setNuevoUsuario({ nombre: '', correo: '', contrasena: '', id_rol: 1 });
  };

  const toggleUsuario = async (id: number, activo: boolean) => {
    const ruta = activo ? `/admin/usuarios/${id}/desactivar` : `/admin/usuarios/${id}/activar`;
    const res = await putAPI(ruta, {}, token);
    mostrarMsg(res?.mensaje || 'Error');
    cargarDatos(token);
  };

  const crearAsignatura = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await postAPI('/admin/asignaturas', nuevaAsignatura, token);
    mostrarMsg(res.mensaje || 'Error');
    cargarDatos(token);
    setNuevaAsignatura({ codigo: '', nombre_materia: '', creditos: 3 });
  };

  const eliminarAsignatura = async (id: number) => {
    const res = await deleteAPI(`/admin/asignaturas/${id}`, token);
    mostrarMsg(res.mensaje);
    cargarDatos(token);
  };

  const crearClase = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await postAPI('/admin/clases', nuevaClase, token);
    mostrarMsg(res.mensaje || 'Error');
    cargarDatos(token);
  };

  const enviarAlerta = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      ...nuevaAlerta,
      id_creador: parseInt(localStorage.getItem('user_id') || '1'),
    };
    const res = await postAPI('/admin/alertas', payload, token);
    mostrarMsg(res.mensaje || 'Error');
    setNuevaAlerta({ titulo: '', mensaje: '', prioridad: 'Media', id_creador: 0 });
  };

  const eliminarAlerta = async (id: number) => {
    const res = await deleteAPI(`/admin/alertas/${id}`, token);
    mostrarMsg(res?.mensaje || 'Error');
    cargarDatos(token);
  };

  const cancelarMatricula = async (id: number) => {
    const res = await deleteAPI(`/admin/matriculas/${id}`, token);
    mostrarMsg(res?.mensaje || 'Error');
    cargarDatos(token);
  };

  // ─── Render ────────────────────────────────────────────────
  return (
    <div className="mx-auto max-w-5xl p-6">
      <h1 className="mb-2 text-2xl font-bold" style={{ color: '#004959' }}>
        Panel Administrador
      </h1>

      {msg && <div className="mb-4 rounded bg-green-100 p-3 text-green-800">{msg}</div>}

      {/* Tabs */}
      <div className="mb-6 flex gap-2 border-b border-gray-200">
        {(['usuarios', 'asignaturas', 'clases', 'alertas'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`rounded-t px-4 py-2 text-sm font-medium capitalize ${tab === t ? 'border-b-2 text-white' : 'text-gray-500 hover:text-gray-700'}`}
            style={tab === t ? { borderColor: '#368FA2', backgroundColor: '#368FA2' } : {}}
          >
            {t}
          </button>
        ))}
      </div>

      {/* ── Usuarios ── */}
      {tab === 'usuarios' && (
        <div className="space-y-6">
          <form
            onSubmit={crearUsuario}
            className="grid grid-cols-2 gap-3 rounded border border-gray-200 p-4"
          >
            <h2 className="col-span-2 font-semibold">Crear usuario</h2>
            <input
              required
              placeholder="Nombre completo"
              value={nuevoUsuario.nombre}
              onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, nombre: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <input
              required
              type="email"
              placeholder="Correo"
              value={nuevoUsuario.correo}
              onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, correo: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <input
              required
              type="password"
              placeholder="Contraseña"
              value={nuevoUsuario.contrasena}
              onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, contrasena: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <select
              value={nuevoUsuario.id_rol}
              onChange={(e) =>
                setNuevoUsuario({ ...nuevoUsuario, id_rol: parseInt(e.target.value) })
              }
              className="rounded border px-3 py-2 text-sm"
            >
              <option value={1}>Estudiante</option>
              <option value={2}>Docente</option>
              <option value={3}>Admin</option>
            </select>
            <button
              type="submit"
              className="col-span-2 rounded py-2 text-sm text-white"
              style={{ backgroundColor: '#368FA2' }}
            >
              Crear usuario
            </button>
          </form>

          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b text-left" style={{ color: '#004959' }}>
                <th className="py-2">Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id_usuario} className="border-b hover:bg-gray-50">
                  <td className="py-2">{u.nombre}</td>
                  <td>{u.correo}</td>
                  <td className="capitalize">{u.rol}</td>
                  <td>
                    <span
                      className={`rounded px-2 py-1 text-xs ${u.activo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}
                    >
                      {u.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <button
                      onClick={() => toggleUsuario(u.id_usuario, u.activo)}
                      className="rounded px-3 py-1 text-xs text-white"
                      style={{ backgroundColor: u.activo ? '#AE443A' : '#368FA2' }}
                    >
                      {u.activo ? 'Desactivar' : 'Activar'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Asignaturas ── */}
      {tab === 'asignaturas' && (
        <div className="space-y-6">
          <form
            onSubmit={crearAsignatura}
            className="grid grid-cols-3 gap-3 rounded border border-gray-200 p-4"
          >
            <h2 className="col-span-3 font-semibold">Crear asignatura</h2>
            <input
              required
              placeholder="Código (ej: MAT-102)"
              value={nuevaAsignatura.codigo}
              onChange={(e) => setNuevaAsignatura({ ...nuevaAsignatura, codigo: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <input
              required
              placeholder="Nombre de la materia"
              value={nuevaAsignatura.nombre_materia}
              onChange={(e) =>
                setNuevaAsignatura({ ...nuevaAsignatura, nombre_materia: e.target.value })
              }
              className="rounded border px-3 py-2 text-sm"
            />
            <input
              required
              type="number"
              placeholder="Créditos"
              value={nuevaAsignatura.creditos}
              onChange={(e) =>
                setNuevaAsignatura({ ...nuevaAsignatura, creditos: parseInt(e.target.value) })
              }
              className="rounded border px-3 py-2 text-sm"
            />
            <button
              type="submit"
              className="col-span-3 rounded py-2 text-sm text-white"
              style={{ backgroundColor: '#368FA2' }}
            >
              Crear asignatura
            </button>
          </form>

          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b text-left" style={{ color: '#004959' }}>
                <th className="py-2">Código</th>
                <th>Nombre</th>
                <th>Créditos</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {asignaturas.map((a) => (
                <tr key={a.id_asignatura} className="border-b hover:bg-gray-50">
                  <td className="py-2">{a.codigo}</td>
                  <td>{a.nombre_materia}</td>
                  <td>{a.creditos}</td>
                  <td>
                    <button
                      onClick={() => eliminarAsignatura(a.id_asignatura)}
                      className="rounded px-3 py-1 text-xs text-white"
                      style={{ backgroundColor: '#AE443A' }}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Clases ── */}
      {tab === 'clases' && (
        <div className="space-y-6">
          <form
            onSubmit={crearClase}
            className="grid grid-cols-2 gap-3 rounded border border-gray-200 p-4"
          >
            <h2 className="col-span-2 font-semibold">Crear clase</h2>
            <select
              required
              value={nuevaClase.id_asignatura}
              onChange={(e) =>
                setNuevaClase({ ...nuevaClase, id_asignatura: parseInt(e.target.value) })
              }
              className="rounded border px-3 py-2 text-sm"
            >
              <option value={0}>Seleccionar asignatura</option>
              {asignaturas.map((a) => (
                <option key={a.id_asignatura} value={a.id_asignatura}>
                  {a.nombre_materia}
                </option>
              ))}
            </select>
            <select
              required
              value={nuevaClase.id_docente}
              onChange={(e) =>
                setNuevaClase({ ...nuevaClase, id_docente: parseInt(e.target.value) })
              }
              className="rounded border px-3 py-2 text-sm"
            >
              <option value={0}>Seleccionar docente</option>
              {usuarios
                .filter((u) => u.rol === 'docente')
                .map((u) => (
                  <option key={u.id_usuario} value={u.id_usuario}>
                    {u.nombre}
                  </option>
                ))}
            </select>
            <input
              required
              placeholder="Periodo (ej: 2026-2)"
              value={nuevaClase.periodo_academico}
              onChange={(e) => setNuevaClase({ ...nuevaClase, periodo_academico: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <input
              required
              placeholder="Grupo (ej: 01)"
              value={nuevaClase.grupo}
              onChange={(e) => setNuevaClase({ ...nuevaClase, grupo: e.target.value })}
              className="rounded border px-3 py-2 text-sm"
            />
            <button
              type="submit"
              className="col-span-2 rounded py-2 text-sm text-white"
              style={{ backgroundColor: '#368FA2' }}
            >
              Crear clase
            </button>
          </form>

          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b text-left" style={{ color: '#004959' }}>
                <th className="py-2">Materia</th>
                <th>Docente</th>
                <th>Periodo</th>
                <th>Grupo</th>
              </tr>
            </thead>
            <tbody>
              {clases.map((c) => (
                <tr key={c.id_clase} className="border-b hover:bg-gray-50">
                  <td className="py-2">{c.nombre_materia}</td>
                  <td>{c.docente}</td>
                  <td>{c.periodo_academico}</td>
                  <td>{c.grupo}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Alertas ── */}
      {tab === 'alertas' && (
        <form onSubmit={enviarAlerta} className="space-y-3 rounded border border-gray-200 p-4">
          <h2 className="font-semibold">Enviar alerta a todos los estudiantes</h2>
          <input
            required
            placeholder="Título"
            value={nuevaAlerta.titulo}
            onChange={(e) => setNuevaAlerta({ ...nuevaAlerta, titulo: e.target.value })}
            className="w-full rounded border px-3 py-2 text-sm"
          />
          <textarea
            required
            placeholder="Mensaje"
            value={nuevaAlerta.mensaje}
            onChange={(e) => setNuevaAlerta({ ...nuevaAlerta, mensaje: e.target.value })}
            className="h-24 w-full rounded border px-3 py-2 text-sm"
          />
          <select
            value={nuevaAlerta.prioridad}
            onChange={(e) => setNuevaAlerta({ ...nuevaAlerta, prioridad: e.target.value })}
            className="rounded border px-3 py-2 text-sm"
          >
            <option value="Alta">Alta</option>
            <option value="Media">Media</option>
            <option value="Baja">Baja</option>
          </select>
          <button
            type="submit"
            className="w-full rounded py-2 text-sm text-white"
            style={{ backgroundColor: '#368FA2' }}
          >
            Enviar alerta
          </button>
        </form>
      )}
    </div>
  );
}
