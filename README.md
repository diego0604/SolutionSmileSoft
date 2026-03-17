
Click public AskDeepWiki 

[![Ask DeepWiki](https://deepwiki.com/badge.svg)]((https://deepwiki.com/diego0604/SolutionSmileSoft)(https://deepwiki.com/diego0604/SolutionSmileSoft))

<p align="center">
  <img src="https://img.icons8.com/color/96/tooth.png" alt="SmileSoft Logo" width="96" height="96"/>
</p>

<h1 align="center">SmileSoft - Sistema de Gestion Odontologica</h1>

<p align="center">
  Plataforma web integral para la gestion de consultorios odontologicos, desarrollada con ASP.NET Core 6.0
</p>

<p align="center">
  <a href="https://github.com/diego0604/SolutionSmileSoft/wiki">
    <img src="https://img.shields.io/badge/Wiki-Documentacion-blue?style=for-the-badge&logo=github" alt="Wiki"/>
  </a>
  <img src="https://img.shields.io/badge/.NET-6.0-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt=".NET 6.0"/>
  <img src="https://img.shields.io/badge/ASP.NET%20Core-MVC%20%2B%20Web%20API-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt="ASP.NET Core"/>
  <img src="https://img.shields.io/badge/SQL%20Server-Database-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="SQL Server"/>
  <img src="https://img.shields.io/badge/Azure-Deploy-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Azure"/>
  <img src="https://img.shields.io/badge/Bootstrap-5.1.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT"/>
  <img src="https://img.shields.io/badge/Swagger-API%20Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger"/>
  <img src="https://img.shields.io/github/license/diego0604/SolutionSmileSoft?style=for-the-badge" alt="License"/>
</p>

---

## Descripcion

**SmileSoft** es un sistema de gestion de consultorios odontologicos que permite administrar pacientes, citas, historias clinicas y usuarios de manera eficiente. El sistema implementa un modelo de control de acceso basado en roles (RBAC) con tres tipos de usuario: **Administrador**, **Odontologo** y **Paciente**.

## Caracteristicas Principales

- **Gestion de Usuarios**: CRUD completo de usuarios con roles diferenciados (Administrador, Odontologo, Paciente).
- **Gestion de Citas**: Ciclo de vida completo de citas (Pendiente, Confirmada, Realizada, Cancelada).
- **Historias Clinicas**: Formularios dinamicos con soporte para preguntas abiertas, cerradas, seleccion multiple y carga de archivos.
- **Autenticacion JWT**: Sistema de autenticacion seguro con tokens JWT.
- **Paneles de Control**: Dashboards personalizados segun el rol del usuario.
- **Almacenamiento en la Nube**: Integracion con Azure Blob Storage para imagenes de historias clinicas.
- **Documentacion API**: Endpoints documentados con Swagger/OpenAPI.
- **CI/CD**: Pipeline de integracion y despliegue continuo con Azure Pipelines.

## Arquitectura

El proyecto sigue un patron de **arquitectura en N capas** (N-Tier) con separacion clara de responsabilidades:

```
SolutionSmileSoft/
|
|-- Application/
|   |-- WebSmileSoft/          # Frontend - ASP.NET Core MVC (Razor Views + Bootstrap)
|   |-- EpSmileSoft/           # Backend  - ASP.NET Core Web API (REST + Swagger)
|
|-- Domain/
|   |-- Domain.Entities/       # Modelos y DTOs
|   |-- Domain.Core/           # Logica de negocio (UsersCore, AppointmentsCore, etc.)
|   |-- Domain.Interfaces/     # Contratos de interfaces (ICore, IRepository)
|
|-- Infrastructure/
|   |-- Repository/            # Patron Repository (acceso a datos)
|   |-- DataAccess/            # Ejecucion SQL y conectividad (ADO.NET)
```

### Diagrama de Flujo de Solicitudes

```
Browser (jQuery/AJAX)
    |
    v
EpSmileSoft (API Controllers)
    |
    v
Domain.Core (Logica de Negocio)
    |
    v
Repository (Acceso a Datos)
    |
    v
DataAccess (Ejecucion SQL)
    |
    v
SQL Server (Base de Datos)
```

## Stack Tecnologico

### Backend

| Componente | Tecnologia | Version |
|---|---|---|
| Framework | ASP.NET Core | 6.0 |
| Documentacion API | Swagger/OpenAPI | Swashbuckle 6.x |
| Autenticacion | JWT Bearer | 6.0.22 |
| Serializacion | Newtonsoft.Json | 13.0.3 |
| Acceso a Datos | ADO.NET | .NET 6 |
| Base de Datos | SQL Server | - |

### Frontend

| Componente | Tecnologia |
|---|---|
| Motor de Vistas | Razor (.cshtml) |
| CSS Framework | Bootstrap 5.1.3 + SB Admin 7.0.4 |
| JavaScript | jQuery, DataTables, SweetAlert2, driver.js |
| Estado del Cliente | sessionStorage |

### Infraestructura

| Componente | Tecnologia |
|---|---|
| Hosting | Azure App Service |
| CI/CD | Azure Pipelines |
| Almacenamiento | Azure Blob Storage |

## Roles de Usuario

| Rol | Descripcion | Permisos Principales |
|---|---|---|
| **Administrador** | Acceso total al sistema | CRUD usuarios, gestion de todas las citas, configuracion del sitio |
| **Odontologo** | Gestion de consultas | Administrar sus citas, crear historias clinicas, actualizar estado de citas |
| **Paciente** | Autoservicio | Ver sus citas, solicitar nuevas citas, consultar su historia clinica |
| **Publico** | Acceso sin autenticacion | Registrarse, iniciar sesion, solicitar cita sin cuenta |

## Endpoints de la API

La API (`EpSmileSoft`) expone los siguientes grupos de endpoints:

| Controlador | Ruta Base | Descripcion |
|---|---|---|
| `SessionController` | `/api/Session/v1/` | Autenticacion y gestion de sesion |
| `UsersController` | `/api/Users/v1/` | Gestion de usuarios |
| `AppointmentsController` | `/api/Appointments/v1/` | Gestion de citas |
| `GenericsController` | `/api/Generics/v1/` | Operaciones genericas (doctores, especialidades, historias clinicas) |
| `BlobsController` | `/api/Blobs/` | Carga de archivos a Azure Blob Storage |

> Para la documentacion interactiva completa de la API, acceder a Swagger en `/swagger` al ejecutar el proyecto.

## Requisitos Previos

- [.NET 6.0 SDK](https://dotnet.microsoft.com/download/dotnet/6.0)
- [SQL Server](https://www.microsoft.com/sql-server)
- [Visual Studio 2022](https://visualstudio.microsoft.com/) (recomendado) o [VS Code](https://code.visualstudio.com/)

## Instalacion y Ejecucion

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/diego0604/SolutionSmileSoft.git
   cd SolutionSmileSoft
   ```

2. **Configurar la cadena de conexion**: Actualizar la cadena de conexion `SmileSoftConnection` en los archivos `appsettings.json` de ambos proyectos (`WebSmileSoft` y `EpSmileSoft`).

3. **Restaurar dependencias y compilar**:
   ```bash
   dotnet restore
   dotnet build
   ```

4. **Ejecutar la API (EpSmileSoft)**:
   ```bash
   dotnet run --project EpSmileSoft
   ```
   La API estara disponible en `https://localhost:7039` y la documentacion Swagger en `https://localhost:7039/swagger`.

5. **Ejecutar la aplicacion web (WebSmileSoft)**:
   ```bash
   dotnet run --project WebSmileSoft
   ```

## Estructura de la Solucion

```
SolutionSmileSoft.sln
|
|-- WebSmileSoft/                  # Aplicacion MVC (Frontend)
|   |-- Controllers/               # Controladores MVC
|   |-- Views/                     # Vistas Razor
|   |-- wwwroot/                   # Archivos estaticos (CSS, JS, imagenes)
|   |-- Models/                    # Modelos de vista
|   |-- ViewComponents/            # Componentes de vista reutilizables
|
|-- EpSmileSoft/                   # Web API (Backend)
|   |-- Controllers/               # Controladores API REST
|   |-- Extensions/                # Extensiones y configuracion
|
|-- Domain.Entities/               # Modelos y DTOs
|   |-- Request/                   # Modelos de solicitud
|   |-- Response/                  # Modelos de respuesta
|
|-- Domain.Core/                   # Logica de negocio
|
|-- Domain.Interfaces/             # Interfaces y contratos
|   |-- Core/                      # Interfaces de logica de negocio
|   |-- Repository/                # Interfaces de repositorios
|   |-- Models/                    # Modelos de interfaz
|
|-- Repository/                    # Implementacion de repositorios
|   |-- Repos/                     # Repositorios concretos
|   |-- Queries/                   # Consultas SQL
|   |-- DataMapper/                # Mapeo de datos
|
|-- DataAccess/                    # Capa de acceso a datos
|
|-- Backup/                        # Respaldos de la solucion
```

## CI/CD

El proyecto utiliza **Azure Pipelines** para integracion y despliegue continuo. La configuracion se encuentra en [`azure-pipelines.yml`](azure-pipelines.yml).

El pipeline incluye:
- Restauracion de paquetes NuGet
- Compilacion con MSBuild
- Ejecucion de pruebas con VSTest
- Despliegue a Azure App Service

## Documentacion

Para documentacion detallada del proyecto, consulta la **[Wiki del proyecto](https://github.com/diego0604/SolutionSmileSoft/wiki)** que incluye:

- Arquitectura del sistema y estructura de la solucion
- Patron de arquitectura por capas
- Sistema de gestion de usuarios
- Sistema de gestion de citas
- Gestion de historias clinicas
- Servicios de API backend
- Capa de acceso a datos
- Tecnologias frontend
- Despliegue y DevOps

---

<p align="center">
  Desarrollado con .NET 6.0 y Azure
</p>
