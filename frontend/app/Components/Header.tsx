'use client';
import Link from 'next/link';
import Exit from '../Components/Exit';

interface Props {
  children: any;
  href: string;
}
const ItemLink = ({ children, href }: Props) => {
  return (
    <li className="grid w-3/4 content-center items-stretch">
      <Link className="bg-secondary w-full rounded-lg p-2 text-center" href={href}>
        {children}
      </Link>
    </li>
  );
};
const Header = () => {
  return (
    <header className="bg-primary text-md fixed flex h-screen w-1/7 flex-col justify-around text-white capitalize">
      <nav className="h-3/4">
        <ul className="mt-8 flex h-full w-full flex-col items-center gap-8">
          <ItemLink href="/dashboard">dashboard</ItemLink>
          <ItemLink href="/horarios">horarios</ItemLink>
          <ItemLink href="/academico">academico</ItemLink>
          <ItemLink href="/comunicacion">comunicacion</ItemLink>
        </ul>
      </nav>
      <div className="flex h-1/4 w-full items-center justify-center">
        <Exit className="w-3/4" />
      </div>
    </header>
  );
};

export default Header;
