# [![surepy](https://socialify.git.ci/benleb/surepy/image?description=1&descriptionEditable=Library%20%26%20CLI%20to%20interact%20with%20the%20Sure%20Petcare%20API%20to%20monitor%20and%20control%20the%20Sure%20Petcare%20Pet%20Door%2FCat%20Flap%20Connect%20%F0%9F%9A%AA%20and%20the%20Pet%20Feeder%20Connect%20%F0%9F%8D%BD&font=KoHo&forks=1&language=1&logo=https%3A%2F%2Femojipedia-us.s3.dualstack.us-west-1.amazonaws.com%2Fthumbs%2F240%2Fapple%2F237%2Fpaw-prints_1f43e.png&pulls=1&stargazers=1)](https://github.com/benleb/surepy)

Library & CLI to interact with the Sure Petcare API. [**surepy**](https://github.com/benleb/surepy) lets you monitor and control the Pet Door/Cat Flap Connect 🚪 and the Pet Feeder Connect 🍽 by [Sure Petcare](https://www.surepetcare.com).

[**surepy**](https://github.com/benleb/surepy) features

🔑 **get an api token** with your account credentials  
🚪 **lock/unlock** a door or flap  
🐾 get the **location** of **pets** & **devices**  
🐈 get the **state** and more attributes of **pets** & **devices**  
🕰️ get **historic** data & events of pets & devices  
📬 get a list of (past) **notifications**  

<!-- > **ToC ·** [Getting Started](#getting-started) · [Usage](#usage)· [Used by](#used-by) · [Acknowledgements](#acknowledgements) **·** [Meta](#meta) -->

## Getting Started

[**surepy**](https://github.com/benleb/surepy) is available via [pypi.org](https://pypi.org)

```bash
python3 -m pip install --upgrade surepy
# or
pip install --upgrade surepy
```

there is also a small cli available
```bash
$ surepy --help
Usage: surepy [OPTIONS] COMMAND [ARGS]...

  surepy cli 🐾

  https://github.com/benleb/surepy

Options:
  --version         show surepy version
  -j, --json        enable json api response output
  -t, --token TEXT  api token
  --help            Show this message and exit.

Commands:
  devices       get devices
  locking       lock control
  notification  get notifications
  pets          get pets
  position      set pet position
  report        get pet/household report
  token         get a token
```
>*the cli probably has some bugs, as it is mainly intended for debugging purposes - be careful* 🐾


<!-- ### Library

see (the not yet written) [docs](https://surepy.readthedocs.io/en/latest/) -->

---

## Used by

* [Sure Petcare](https://www.home-assistant.io/integrations/surepetcare/) integration in [Home Assistant](https://www.home-assistant.io/)

Feel free to add you project!

## Acknowledgments

* Thanks to all the people who provided information about devices I do not own myself, thanks!
* Thanks to [@rcastberg](https://github.com/rcastberg) for hist previous work on the [Sure Petcare](https://www.surepetcare.com) API ([github.com/rcastberg/sure_petcare](https://github.com/rcastberg/sure_petcare))
* Thanks to [@wei](https://github.com/wei) for the  header image generator ([github.com/wei/socialify](https://github.com/wei/socialify))

## Meta

**Ben Lebherz**: *cat lover 🐾 developer & maintainer* - [@benleb](https://github.com/benleb) | [@ben_leb](https://twitter.com/ben_leb)

<!-- See also the list of [contributors](CONTRIBUTORS) who participated in this project. -->

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
