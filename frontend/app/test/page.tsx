'use client';
import { useRouter } from 'next/navigation';
// import { login } from "../lib/api";
import { useState } from 'react';
export default function page() {
  return (
    <form>
      <label htmlFor="mail">mail:</label>
      <input name="mail" type="email" className="border-2 border-black" />
      <label htmlFor="password">password</label>
      <input name="password" type="password" />
      <button>ingresar</button>
    </form>
  );
}
