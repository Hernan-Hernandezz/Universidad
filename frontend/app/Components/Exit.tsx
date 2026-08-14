import { useRouter } from "next/navigation";
interface Props {
  className: string;
}
const Exit = ({ className }: Props) => {
  const router = useRouter();
  const salir = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };
  return (
    <button className={`p-2  bg-secondary ${className}`} onClick={salir}>
      salir
    </button>
  );
};

export default Exit;
