"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "../lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const Dashboard = () => {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    const academic_summary = fetchAPI("/user/academic_summary", token);
    const horarios = fetchAPI("/user/horarios", token);
  }, []);
  const salir = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <form>
        <button onClick={salir}>salir</button>
      </form>
    </div>
  );
};

export default Dashboard;
