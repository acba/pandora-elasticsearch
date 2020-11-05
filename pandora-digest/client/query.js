const { Client } = require('@elastic/elasticsearch')
const client = new Client({ node: 'http://localhost:9200' })

async function run () {
    // // Let's start by indexing some data
    // await client.index({
    //   index: 'game-of-thrones',
    //   body: {
    //     character: 'Ned Stark',
    //     quote: 'Winter is coming.'
    //   }
    // })
  
    // await client.index({
    //   index: 'game-of-thrones',
    //   body: {
    //     character: 'Daenerys Targaryen',
    //     quote: 'I am the blood of the dragon.'
    //   }
    // })
  
    // await client.index({
    //   index: 'game-of-thrones',
    //   body: {
    //     character: 'Tyrion Lannister',
    //     quote: 'A mind needs books like a sword needs a whetstone.'
    //   }
    // })
  
    // // here we are forcing an index refresh, otherwise we will not
    // // get any result in the consequent search
    // await client.indices.refresh({ index: 'game-of-thrones' })
  
    // Let's search!
    const resultado = await client.search({
      index: 'diario-oficial',
      body: {
        query: {
          match: { texto: '119.960.518-22' }
        }
      }
    })
  
    console.log(resultado)
    const hits = resultado.body.hits.hits.map(x => {
        return {
            score: x._score,
            pagina: x._source.pagina,
            texto: x._source.texto,
            criado: x._source.criado,
            filename: x._source.filename,
            hostname: x._source.hostname,
            // attachment: x._source.attachment,
        }
    })

    console.log('##### HITS ######')
    console.log(hits)
  }
  
  run().catch(console.log)
  