# eg0n-frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

Install Node.js version 18.3 or higher (depends by your distro/OS)
(https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

install npm:  npm install -g npm

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev

start a local web server: http://localhost:5173
```

### Compile and Minify for Production

```sh
npm run build
```

### how to use with django eg0n-portal

```sh
python manage.py runserver

npm run dev
```

this command execute in separate shell allow user to run django and vite for development
in production we change js link from django template with static js build file.