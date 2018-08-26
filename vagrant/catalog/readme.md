## Catalogo App
Página web de catálogo de material esportivo. Os materiais são separados e exibidos de acordo com a sua categoria.

### Pré-requisito
* Ter um web browser instalado como o [Chrome](https://www.google.pt/intl/pt-PT/
chrome/?brand=CHBD&gclid=EAIaIQobChMI3Iuek8H32gIVDBGRCh3xvwoQEAAYASAAEgK3MPD_
BwE&gclsrc=aw.ds&dclid=CIDp5pnB99oCFY9HhgodXyAAhw).
* Instalar a máquina virtual - ver tópico de Instalação.

### Instalação
1. Instalar o [Vagrant](https://www.vagrantup.com/) e o [VitrualBox](https://www.virtualbox.org/);
2. Clonar a [fullstack-nanodegree-vm](https://github.com/rdalas/fullstack-nanodegree-vm.git);
3. No CMD ou Terminal navegue até a pasta (fullstack-nanodegree-vm/vagrant) e inicie a VM Vagrant  com o comando *vagrant up*. Após iniciar a VM use o comando *vagrant ssh*;
4. Execute seu aplicativo dentro da VM  com o comando *python /vagrant/catalog/catalogo.py*.

### Utilizando o App
Acesse o aplicativo visitando http://localhost:8000 localmente, navegue pelos produtos e categorias e caso precise alterar, criar um novo registro ou deletar um item, faça o Login com uma conta do google clicando no botão *Login*.

### API
O aplicativo possui uma API visitando http://localhost:8000/catalog/JSON.

### Built With
* **Python** - *Linguagem de Programação*
* **Flask** - *The Web Framework*
* **SQL Alchemy** - *The Python SQL Toolkit and Object Relational Mapper*
* **HTML** - *HyperText Markup Language*
* **CSS** - *Cascading Style Sheets*

### Autor
* **Rodrigo Dalamangas** - *Initial Work*
