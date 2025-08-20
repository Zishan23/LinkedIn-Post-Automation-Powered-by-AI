import { NavLink } from "react-router-dom";
export default function Navbar() {
    return(
        <>
        <nav className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white p-4 shadow-lg">
            <div className="max-width p-4 flex justify-center items-center">
                <div className="flex justify-center items-center w-full">
                    <div className="flex">
                                                 <NavLink to="/" className="flex justify-center items-center">
                             <img src="/logo.png" alt="Logo" className="h-24 sm:h-28 w-auto drop-shadow-[0_0_28px_rgba(20,184,166,0.8)]"/>
                         </NavLink>
                    </div>

                    {/* <div>
                        <NavLink to="/postanalysis" className="font-montserrat px-4 py-3 rounded-full hover:bg-slate-200 hover:font-semibold transition-all">Analyse Posts</NavLink>
                    </div> */}
                </div>    
            </div>
        </nav>
        </>
    );
}
