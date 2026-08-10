import { useRouter } from "next/navigation";
const Exit = () => {
  const router = useRouter();
  const salir = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };
  return (
    <button className="p-2 border-2 bg-blue-400" onClick={salir}>
      salir
    </button>
  );
};

export default Exit;
