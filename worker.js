/**
 * DEPRECATED — This Cloudflare Worker is no longer used.
 * The contact form now submits to Google Apps Script.
 * See contact.html line 249 for the active endpoint.
 * 
 * This file is kept for reference only.
 * If you need to re-enable, restrict CORS to "https://datrey.ma".
 */
export default {
  async fetch(request, env, ctx) {
    // Handling CORS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    try {
      const formData = await request.json();
      const { name, email, phone, subject, message } = formData;

      if (!name || !email || !message) {
        return new Response(JSON.stringify({ error: "Missing required fields" }), {
          status: 400,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }

      // Configure MailChannels payload
      const payload = {
        personalizations: [
          {
            to: [{ email: "contact@datrey.ma", name: "DatRey Contact" }],
          },
        ],
        from: {
          email: "noreply@datrey.ma", // Must match your domain
          name: "DatRey Website",
        },
        reply_to: {
          email: email,
          name: name,
        },
        subject: `Nouveau lead : ${subject || "Contact DatRey.ma"}`,
        content: [
          {
            type: "text/plain",
            value: `Nouveau message depuis DatRey.ma\n\nNom: ${name}\nEmail: ${email}\nTéléphone: ${phone || "Non renseigné"}\nSujet: ${subject}\n\nMessage:\n${message}`,
          },
        ],
      };

      const response = await fetch("https://api.mailchannels.net/tx/v1/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.status === 202 || response.ok) {
        return new Response(JSON.stringify({ success: true, message: "Email envoyé avec succès" }), {
          status: 200,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      } else {
        const errorText = await response.text();
        return new Response(JSON.stringify({ error: "Erreur lors de l'envoi", details: errorText }), {
          status: 500,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }
    } catch (error) {
      return new Response(JSON.stringify({ error: "Erreur serveur", details: error.message }), {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }
  },
};
