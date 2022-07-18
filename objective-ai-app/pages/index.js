import Head from 'next/head'
import Image from 'next/image'
import Script from 'next/script'

import { withAuthenticator, cHeading } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import '@aws-amplify/ui-react/styles.css';
import styles from '../styles/Home.module.css'
import awsExports from '../src/aws-exports';
Amplify.configure(awsExports);



function Home(signOut, user) {
  console.log(user);
  return (
    <div className={styles.container}>
      
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW"
        crossOrigin="anonymous"
      />
      <InitializeApp user={user}/>
      
      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}


function InitializeApp(user) {
  function handleClick(event){
   console.log() 
  }

  return (
    <div className="container">
      <div className="d-flex justify-content-center">  
        <button onClick={handleClick}>Initialize Account</button>
      </div>
    </div>
    );
}

export default withAuthenticator(Home);
// export default Home;
