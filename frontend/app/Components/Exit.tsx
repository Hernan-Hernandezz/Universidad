import { useRouter } from 'next/navigation';
interface Props {
  className: string;
}
const Exit = ({ className }: Props) => {
  const router = useRouter();
  const salir = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };
  return (
    <button className={`bg-secondary p-2 hover:cursor-pointer ${className}`} onClick={salir}>
      salir
    </button>
  );
};

export default Exit;
