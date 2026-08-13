import Link from "next/link";
import Exit from "../Components/Exit";

const ItemLink = ({ children, href }) => {
  return (
    <li className="bg-secondary w-3/4 text-center p-2 rounded-lg">
      <Link href={href}>{children}</Link>
    </li>
  );
};
const Header = () => {
  return (
    <header className="h-screen w-40 bg-primary  text-white text-md capitalize flex flex-col justify-around">
      <nav className="h-1/2">
        <ul className="flex h-full justify-around items-center flex-col">
          <ItemLink href="/dashboard">dashboard</ItemLink>
          <ItemLink href="/horarios">horarios</ItemLink>
          <ItemLink href="/academico">academico</ItemLink>
          <ItemLink href="/comunicacion">comunicacion</ItemLink>
        </ul>
      </nav>
      <div className="h-1/2">
        <Exit />
      </div>
    </header>
  );
};

export default Header;
