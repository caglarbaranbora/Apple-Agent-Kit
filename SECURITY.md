# Security Policy

## Desteklenen Sürümler

Apple Agent Kit şu an 0.x geliştirme aşamasındadır. Güvenlik yamaları en son yayınlanan sürüme uygulanır.

| Sürüm   | Destekleniyor mu |
| ------- | ----------------- |
| 0.1.x   | ✅                 |
| < 0.1   | ❌                 |

## Güvenlik Açığı Bildirme

Bir güvenlik açığı bulduysanız **lütfen public bir issue açmayın.**

Bunun yerine:

1. GitHub'ın [Private Vulnerability Reporting](https://github.com/caglarbaranbora/Apple-Agent-Kit/security/advisories/new) özelliğini kullanarak bildirin, **veya**
2. [maintainer e-postası buraya] adresine detaylı bir açıklama gönderin.

Bildiriminizde şunları içermeye çalışın:
- Açığın kısa açıklaması
- Etkilenen dosya/Skill/Knowledge Contract
- Tekrar üretme adımları (mümkünse)
- Potansiyel etki

## Yanıt Süreci

- 48 saat içinde bildiriminizi aldığımızı teyit etmeye çalışıyoruz.
- Doğrulanan açıklar için bir düzeltme takvimi paylaşılır.
- Açık, düzeltme yayınlandıktan sonra kamuya duyurulur (istenirse bildiren kişiye kredi verilir).

## Kapsam

Bu repo bir npm installer (`npx apple-agent-kit`) ve Claude Code plugin marketplace'i içerir. Özellikle şu noktalara dikkat edin:
- `bin/install.js` içindeki komut çalıştırma / dosya yazma davranışı
- Marketplace/plugin manifest'inin kötü amaçlı Skill/Knowledge Contract enjekte edilmesine karşı bütünlüğü
