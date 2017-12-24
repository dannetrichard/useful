const puppeteer = require('puppeteer')
const fs = require('fs')
const URL = require('url').URL
const md5=require("md5")  

var mysql = require('mysql')
var connection = mysql.createConnection({
  host: '106.14.212.44',
  user: 'root',
  password: 'jinjun123',
  database: 'soup'
})

connection.connect()

connection.query('SELECT xz_id,picture,description from items where pid = 16 and mid = 601 limit 1', function (error, results, fields) {
  if (error) throw error
  let result = results[0]
  result['picture'] = JSON.parse(result['picture'])
  result['description'] = JSON.parse(result['description'])
  let h1 = '<div class="picture"><img src="' + result['picture'].join('"><img src="') + '"></div>'
  let h2 = '<div class="description"><img src="' + result['description'].join('"><img src="') + '"></div>'

  fs.writeFileSync('picture.html', h1 + h2)
  downloadImgs(result)
})

connection.end()

var isHasElement = function (arr, value) {
  for (let i = 0, vlen = arr['picture'].length; i < vlen; i++) {
    if (arr['picture'][i] === value) {
      //let split = value.split('.')
      // return 'picture/' + i + '.' + split[split.length - 1]
      return 'picture/' + md5(i) + '.TBI'
    }
  }
  for (let i = 0, vlen = arr['description'].length; i < vlen; i++) {
    if (arr['description'][i] === value) {
      let split = value.split('.')
      return 'description/' + i + '.' + split[split.length - 1]
    }
  }
  return -1
}

var downloadImgs = async function (result) {
  const browser = await puppeteer.launch({executablePath: 'E:/chrome-win32/chrome.exe', headless: false})
  const page = await browser.newPage()
  page.on('response', async (resp) => {
    let url = new URL(resp.url)
    if (url['href'] === 'file:///G:/node/picture.html') {
      return -1
    }
    let filename = isHasElement(result, url['href'])
    if (filename !== -1) {
      const buffer = await resp.buffer()
      fs.writeFileSync(filename, buffer)
    }
  })
  await page.goto('file:///G:/node/picture.html')
}