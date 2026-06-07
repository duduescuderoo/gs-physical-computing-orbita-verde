# 🌍 OrbitaVerde — Detecção de Fumaça e Fogo por Visão Computacional

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-4.13-green?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-2.4-orange?style=for-the-badge&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/FIAP-Global%20Solution%202026-red?style=for-the-badge"/>
</p>

---

## 📌 Sobre o Projeto

O **OrbitaVerde** é um sistema de visão computacional desenvolvido para a **Global Solution 2026 da FIAP**, com tema **Indústria Espacial / Economia Espacial**.

A solução simula um **sensor visual de solo** que detecta fumaça e fogo em tempo real a partir de vídeo, funcionando como camada complementar ao monitoramento feito por satélites da NASA e ESA. Quando um satélite identifica uma anomalia térmica em determinada região, câmeras no solo com este sistema confirmam e classificam o nível de risco localmente.

> *"Resolver problemas no espaço nos ensina a resolver problemas na Terra."*
> — Kickoff GS 2026, FIAP

---

## 🛰️ Contexto — Plataforma OrbitaVerde

Este módulo faz parte de uma plataforma maior chamada **OrbitaVerde**, que integra:

| Camada | Tecnologia | Função |
|---|---|---|
| Satélite | NASA FIRMS / ESA Copernicus | Detecção de anomalias térmicas em escala global |
| Solo (este módulo) | Python + OpenCV | Confirmação visual e classificação local de risco |
| Backend | C# / ASP.NET Core | Processamento e orquestração dos alertas |
| Mobile | App | Notificações para agentes de campo e população |

---

## 🔥 Como funciona a detecção

O sistema analisa cada frame do vídeo utilizando o espaço de cores **HSV** (Hue, Saturation, Value), que permite separar com mais precisão as cores características de fogo e fumaça independentemente da iluminação do ambiente.

### Pipeline de Visão Computacional

```
[Frame do vídeo]
       ↓
[Conversão BGR → HSV]
       ↓
┌──────────────────┐     ┌──────────────────────┐
│  Máscara de FOGO │     │  Máscara de FUMAÇA   │
│  H: 0–35         │     │  S: < 50, V: 150–220 │
│  S: > 100        │     │  (tons cinza/branco)  │
│  (laranja/vermelho)│   └──────────────────────┘
└──────────────────┘
       ↓
[Limpeza morfológica (abertura + dilatação)]
       ↓
[Extração de contornos]
       ↓
[Filtro por área mínima (> 500px²)]
       ↓
[Bounding boxes + labels na tela]
       ↓
[Cálculo de nível de risco por cobertura de tela]
       ↓
[Exibição em tempo real + log no terminal]
```

### Níveis de Risco

| Nível | Condição | Cor |
|---|---|---|
| 🟢 NORMAL | Nenhuma detecção relevante | Verde |
| 🟡 ALERTA | 3–10% da tela com detecção | Laranja |
| 🔴 PERIGO | > 10% da tela com detecção | Vermelho |

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.10+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/orbita-verde-cv.git
cd orbita-verde-cv

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Com arquivo de vídeo
python main.py --video caminho/para/video.mp4

# Com webcam
python main.py --webcam
```

> Pressione **`Q`** para encerrar.

---

## 📁 Estrutura do Projeto

```
PhysicalComputing_GS/
│
├── main.py                 # Script principal — captura e pipeline
├── detector.py             # Lógica de detecção via máscaras HSV
├── utils.py                # Renderização visual e cálculo de risco
├── gerar_video_teste.py    # Gerador de vídeo sintético para testes
│
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

---

## 📦 Dependências

```
opencv-python
numpy
```

---

## 🌱 Conexão com os ODS da ONU

Este projeto contribui diretamente para:

- **ODS 13** — Ação contra a mudança global do clima *(monitoramento de queimadas)*
- **ODS 11** — Cidades e comunidades sustentáveis *(alertas em tempo real)*
- **ODS 9** — Indústria, inovação e infraestrutura *(tecnologia de detecção visual)*

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| Davi Vieira | RM556798 |
| Luca Monteiro | RM556906 |
| Arthur Silva | RM553320 |
| Eduardo Escudero | RM556527 |

**Turma:** [sua turma]
**Curso:** [seu curso]
**Disciplina:** Physical Computing: IoT & IoB
**Professor:** [nome do professor]

---

## 🏫 Instituição

**FIAP — Faculdade de Informática e Administração Paulista**
Global Solution | 1º Semestre de 2026
