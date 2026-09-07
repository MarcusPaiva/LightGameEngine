# LightGameEngine 🎮✨

**Um canivete suíço para o Pygame — não um substituto.**

LightGameEngine é uma camada leve, em Python, construída em cima do Pygame: pega o que o Pygame já faz bem e embrulha do jeito mais simples e reutilizável possível, adicionando por cima os recursos que o Pygame **não** traz nativamente — efeitos prontos, um sistema de input mais confortável e objetos de jogo (botão, modal...) que hoje todo mundo acaba reinventando do zero em cada projeto novo.

A ideia não é competir com engines completas (Godot, Unity) nem esconder o Pygame de você. Você continua programando em Pygame puro — a lib só poupa o boilerplate repetido projeto após projeto.

## 🎯 Filosofia

LightGameEngine é pensada para ser uma ferramenta de **alto nível**, feita para facilitar a vida de quem programa jogos em Python — **não** para substituir o Pygame. Você mantém acesso total a ele sempre que precisar; a lib só evita que você reescreva, toda vez, o que já devia vir pronto: colisão, input, UI básica, efeitos.

## 🧰 O que a lib entrega hoje

- **Geometria e colisão**, sem depender do Pygame para a matemática (`BoundingBox`, `RectBoundingBox`, `CircleBoundingBox`, detecção de colisão círculo-círculo).
- **Wrappers finos** e encadeáveis sobre janela, fontes, imagens e som (`SurfaceScreen`, `GameFont`, `Image`, `SoundEffect`, `Music`).
- **Efeitos e recursos extras** que o Pygame não tem de fábrica — hoje: fade in/out de imagem, pronto para splash screens.
- **Melhoria de uso em inputs**: um enum `Keys` com nome legível para cada tecla do Pygame (incluindo aliases como `key_up`), uma classe `Keyboard` que já rastreia as teclas pressionadas a cada frame, e helpers de mouse (posição, clique) prontos para usar.
- **Objetos semi-prontos para uso**: `Button` e `Modal`, componentes de UI comuns em praticamente todo jogo (menus, confirmações, diálogos) que normalmente você monta na mão.

Ideal para prototipagem rápida, ensino de programação de jogos, ou simplesmente para quem gosta de colocar a mão no código sem precisar reinventar a roda.

## 📌 Recursos em desenvolvimento

- Gerenciamento de cenas totalmente encapsulado
- Mais objetos de UI prontos para uso
- SplashScreen pronta para uso (hoje já disponível como efeito de fade de imagem)
- Suporte a assets com cache

> Projeto em estágio inicial – acompanhe os posts semanais no [meu LinkedIn](https://www.linkedin.com/in/marcuspaiva/) para ver o progresso e participe com feedbacks!

🚧 **Em construção – contribuições e sugestões são bem-vindas!**
