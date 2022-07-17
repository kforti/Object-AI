import "bootstrap/dist/css/bootstrap.css";

import '../styles/globals.css'

import { useEffect } from "react";
import { useRouter } from "next/router";


function MyApp({ Component, pageProps }) {
  useEffect(() => {
    import('bootstrap')
  }, [])
  return <Component {...pageProps} />
}

export default MyApp
